import os
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

# Configure an isolated database before importing application modules.
_directory = tempfile.TemporaryDirectory()
os.environ["INSPECTION_TRACKER_DB"] = str(Path(_directory.name) / "inspections.db")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidget
from sqlalchemy.exc import OperationalError

from database import Base, DATABASE_PATH, SessionLocal, engine
from inspection_service import create_inspection, get_inspections
from ui.dashboard import Dashboard
from ui.inspection_dialog import InspectionDialog


class DesktopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        engine.dispose()
        _directory.cleanup()

    def add(self, client="Example", days=3, price=120):
        with SessionLocal() as session:
            return create_inspection(
                session, client, "100 Main St", "Quarterly", date.today(),
                date.today() + timedelta(days=days), price,
            )

    def test_add_edit_complete_and_delete_through_dialog(self):
        dialog = InspectionDialog()
        dialog.form.client_name.setText("Example")
        dialog.form.location.setText("100 Main St")
        dialog.form.frequency.setCurrentText("Quarterly")
        dialog.perform("save")
        self.assertEqual(dialog.result(), QDialog.DialogCode.Accepted)
        with SessionLocal() as session:
            inspection = get_inspections(session)[0]
        edit = InspectionDialog(inspection)
        edit.form.client_name.setText("Updated")
        edit.form.price.setValue(150)
        edit.perform("save")
        with SessionLocal() as session:
            updated = get_inspections(session)[0]
            self.assertEqual(updated.client_name, "Updated")
            self.assertEqual(updated.price, 150)
        complete = InspectionDialog(updated)
        complete.perform("complete")
        with SessionLocal() as session:
            items = get_inspections(session)
            self.assertEqual(len(items), 2)
            original = next(item for item in items if item.id == inspection.id)
            next_item = next(item for item in items if item.id != inspection.id)
            self.assertEqual(original.performed_date, date.today())
            self.assertGreater(next_item.scheduled_date, original.scheduled_date)
        delete = InspectionDialog(next_item)
        with patch.object(QMessageBox, "question", return_value=QMessageBox.StandardButton.Yes):
            delete.perform("delete")
        with SessionLocal() as session:
            self.assertEqual(len(get_inspections(session)), 1)

    def test_validation_and_database_failure_keep_dialog_open(self):
        dialog = InspectionDialog()
        with patch.object(QMessageBox, "warning") as warning:
            dialog.perform("save")
            warning.assert_called_once()
        dialog.form.client_name.setText("Example")
        dialog.form.location.setText("Location")
        error = OperationalError("INSERT", {}, Exception("database is locked"))
        with patch("ui.inspection_dialog.create_inspection", side_effect=error), patch.object(QMessageBox, "warning") as warning:
            dialog.perform("save")
            self.assertIn("database is busy", warning.call_args.args[2])
        self.assertEqual(dialog.result(), QDialog.DialogCode.Rejected)
        with SessionLocal() as session:
            self.assertEqual(get_inspections(session), [])

    def test_dashboard_sorting_preserves_row_identity_and_read_only(self):
        self.add("Zebra", -1, 20)
        self.add("Alpha", 3, 100)
        window = Dashboard()
        table = window.findChild(QTableWidget)
        self.assertEqual(table.rowCount(), 2)
        table.sortItems(6, Qt.SortOrder.DescendingOrder)
        self.assertEqual(table.item(0, 1).text(), "Alpha")
        with patch.object(window, "open_inspection") as opened:
            table.cellClicked.emit(0, 1)
            self.assertEqual(opened.call_args.args[0].client_name, "Alpha")
            self.assertTrue(opened.call_args.kwargs["read_only"])
        with SessionLocal() as session:
            item = get_inspections(session)[0]
        dialog = InspectionDialog(item, read_only=True)
        self.assertFalse(dialog.form.isEnabled())
        window.close()

    def test_database_location_and_wal(self):
        self.assertEqual(DATABASE_PATH, Path(os.environ["INSPECTION_TRACKER_DB"]))
        with engine.connect() as connection:
            self.assertEqual(connection.exec_driver_sql("PRAGMA journal_mode").scalar(), "wal")
            self.assertEqual(connection.exec_driver_sql("PRAGMA busy_timeout").scalar(), 5000)


if __name__ == "__main__":
    unittest.main()

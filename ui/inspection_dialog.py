import logging
from datetime import date

from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from inspection_service import create_inspection, update_inspection, complete_inspection, delete_inspection
from models import Inspection
from ui.inspection_form import InspectionForm


def show_database_error(parent, error):
    logging.exception("Database operation failed")
    message = "The database operation failed. See the application log for details."
    if "locked" in str(error).lower() or "busy" in str(error).lower():
        message = "The database is busy. Close other apps using this database and try again."
    QMessageBox.warning(parent, "Database error", message)


class InspectionDialog(QDialog):
    def __init__(self, inspection=None, read_only=False, parent=None):
        super().__init__(parent)
        self.inspection_id = inspection.id if inspection else None
        self.setWindowTitle(inspection.client_name if inspection else "Add New Inspection")
        self.setMinimumWidth(480)
        layout = QVBoxLayout(self)
        self.form = InspectionForm(inspection)
        layout.addWidget(self.form)
        if inspection and inspection.performed_date:
            layout.addWidget(QLabel(f"Performed: {inspection.performed_date}"))
        buttons = QHBoxLayout()
        layout.addLayout(buttons)
        if read_only:
            self.form.setEnabled(False)
        else:
            save = QPushButton("Apply Changes" if inspection else "Add Inspection")
            save.clicked.connect(lambda: self.perform("save"))
            buttons.addWidget(save)
            if inspection:
                complete = QPushButton("Complete Inspection")
                complete.setEnabled(inspection.performed_date is None)
                complete.clicked.connect(lambda: self.perform("complete"))
                buttons.addWidget(complete)
                delete = QPushButton("Delete Inspection")
                delete.clicked.connect(lambda: self.perform("delete"))
                buttons.addWidget(delete)
        close = QPushButton("Close" if read_only else "Cancel")
        close.clicked.connect(self.reject)
        buttons.addWidget(close)

    def perform(self, action):
        if action == "delete" and QMessageBox.question(
            self, "Delete inspection", "Delete this inspection? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        ) != QMessageBox.StandardButton.Yes:
            return
        try:
            values = self.form.values() if action == "save" else None
            with SessionLocal() as session:
                if self.inspection_id is None:
                    create_inspection(session, start_date=self.form.start_date.date().toPython(), **values)
                else:
                    inspection = session.get(Inspection, self.inspection_id)
                    if inspection is None:
                        raise ValueError("Inspection not found. Refresh the dashboard.")
                    if action == "save":
                        update_inspection(session, inspection, **values)
                    elif action == "complete":
                        if inspection.performed_date is not None:
                            raise ValueError("This inspection has already been completed.")
                        complete_inspection(session, inspection, date.today())
                    elif action == "delete":
                        delete_inspection(session, inspection)
        except ValueError as error:
            QMessageBox.warning(self, "Check inspection", str(error))
            return
        except SQLAlchemyError as error:
            show_database_error(self, error)
            return
        self.accept()

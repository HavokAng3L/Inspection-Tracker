import logging
import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from database import DATABASE_PATH, Base, engine
from ui.dashboard import Dashboard


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Inspection Tracker")
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QWidget { font-size: 14px; }
        QLabel#title { font-size: 26px; font-weight: bold; }
        QLabel#count { font-size: 30px; font-weight: bold; }
        QGroupBox { font-weight: bold; margin-top: 12px; padding-top: 18px; }
        QPushButton { padding: 8px 12px; }
        QPushButton#inspectionCard { text-align: left; padding: 14px; }
    """)
    logging.basicConfig(
        filename=DATABASE_PATH.parent / "inspection-tracker.log",
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
    )
    try:
        Base.metadata.create_all(engine)
        window = Dashboard()
    except Exception:
        logging.exception("Application startup failed")
        QMessageBox.critical(None, "Startup error", "Unable to start Inspection Tracker. See inspection-tracker.log in the database folder.")
        return 1
    window.show()
    result = app.exec()
    engine.dispose()
    return result


if __name__ == "__main__":
    sys.exit(main())

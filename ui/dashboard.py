from PySide6.QtWidgets import (
    QDialog, QGroupBox, QHBoxLayout, QLabel, QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget,
)
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from inspection_service import get_overdue_inspections, get_due_soon_inspections, get_upcoming_inspections, get_inspections
from ui.inspection_cards import show_inspection_section
from ui.inspection_table import show_inspection_table
from ui.inspection_dialog import InspectionDialog, show_database_error


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inspection Tracker (MINI)")
        self.resize(1100, 850)
        self.refresh()

    def refresh(self):
        try:
            with SessionLocal() as session:
                groups = [
                    ("Overdue", get_overdue_inspections(session)),
                    ("Due Soon", get_due_soon_inspections(session)),
                    ("Upcoming", get_upcoming_inspections(session)),
                ]
                inspections = get_inspections(session)
        except SQLAlchemyError as error:
            show_database_error(self, error)
            if self.centralWidget() is None:
                retry = QPushButton("Retry loading dashboard")
                retry.clicked.connect(self.refresh)
                self.setCentralWidget(retry)
            return
        content = QWidget()
        layout = QVBoxLayout(content)
        header = QLabel("Inspection Tracker (MINI)")
        header.setObjectName("title")
        layout.addWidget(header)
        layout.addWidget(QLabel("Welcome to V1 of Inspection Tracker (MINI)"))
        actions = QHBoxLayout()
        add = QPushButton("Add Inspection")
        add.clicked.connect(lambda: self.open_inspection())
        actions.addWidget(add)
        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self.refresh)
        actions.addWidget(refresh)
        actions.addStretch()
        layout.addLayout(actions)
        counts = QHBoxLayout()
        for title, items in groups:
            card = QGroupBox(title)
            card_layout = QVBoxLayout(card)
            number = QLabel(str(len(items)))
            number.setObjectName("count")
            card_layout.addWidget(number)
            counts.addWidget(card)
        layout.addLayout(counts)
        for title, items in groups:
            layout.addWidget(show_inspection_section(f"{title} Inspections", items, self.open_inspection))
        layout.addWidget(QLabel("All Inspections"))
        layout.addWidget(show_inspection_table(
            inspections, lambda item: self.open_inspection(item, read_only=True),
        ))
        layout.addStretch()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)
        self.setCentralWidget(scroll)

    def open_inspection(self, inspection=None, read_only=False):
        dialog = InspectionDialog(inspection, read_only, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh()
            self.statusBar().showMessage("Inspection saved successfully.", 5000)

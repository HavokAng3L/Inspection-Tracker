from datetime import date

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QComboBox, QDateEdit, QDoubleSpinBox, QFormLayout, QLineEdit, QTextEdit, QWidget,
)


class InspectionForm(QWidget):
    def __init__(self, inspection=None, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        self.client_name = QLineEdit(inspection.client_name if inspection else "")
        self.location = QLineEdit(inspection.location if inspection else "")
        self.frequency = QComboBox()
        self.frequency.addItems(["Annual", "Semi-Annual", "Quarterly"])
        if inspection:
            self.frequency.setCurrentText(inspection.frequency)
        self.start_date = self.date_field(inspection.start_date if inspection else date.today())
        self.scheduled_date = self.date_field(inspection.scheduled_date if inspection else date.today())
        self.price = QDoubleSpinBox()
        self.price.setRange(0, 999999999.99)
        self.price.setDecimals(2)
        self.price.setPrefix("$")
        self.price.setValue(inspection.price if inspection else 0)
        self.notes = QTextEdit((inspection.notes or "") if inspection else "")
        self.notes.setMaximumHeight(120)
        for label, widget in [
            ("Client Name", self.client_name), ("Location", self.location),
            ("Frequency", self.frequency), ("Start Date", self.start_date),
            ("Scheduled Date", self.scheduled_date), ("Price", self.price),
            ("Notes", self.notes),
        ]:
            layout.addRow(label, widget)
        if inspection:
            self.start_date.setEnabled(False)

    @staticmethod
    def date_field(value):
        field = QDateEdit(QDate(value.year, value.month, value.day))
        field.setCalendarPopup(True)
        field.setDisplayFormat("yyyy-MM-dd")
        return field

    def values(self):
        client = self.client_name.text().strip()
        location = self.location.text().strip()
        if not client or not location:
            raise ValueError("Client name and location are required.")
        return dict(
            client_name=client, location=location,
            frequency=self.frequency.currentText(),
            scheduled_date=self.scheduled_date.date().toPython(),
            price=self.price.value(), notes=self.notes.toPlainText().strip() or None,
        )

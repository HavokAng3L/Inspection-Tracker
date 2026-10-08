from PySide6.QtWidgets import QGroupBox, QLabel, QPushButton, QVBoxLayout


def show_inspection_section(title, inspections, on_open):
    section = QGroupBox(title)
    layout = QVBoxLayout(section)
    for inspection in inspections:
        card = QPushButton(
            f"{inspection.client_name}\nLocation: {inspection.location}\n"
            f"Scheduled: {inspection.scheduled_date}\nPrice: ${inspection.price:.2f}"
        )
        card.setObjectName("inspectionCard")
        card.clicked.connect(lambda checked=False, item=inspection: on_open(item))
        layout.addWidget(card)
    if not inspections:
        layout.addWidget(QLabel("No inspections in this period."))
    return section

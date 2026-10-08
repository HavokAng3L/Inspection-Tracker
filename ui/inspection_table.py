from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidget, QTableWidgetItem


class SortableItem(QTableWidgetItem):
    def __init__(self, label, value):
        super().__init__(label)
        self.sort_value = value

    def __lt__(self, other):
        return self.sort_value < other.sort_value


def show_inspection_table(inspections, on_open):
    table = QTableWidget(len(inspections), 7)
    table.setHorizontalHeaderLabels([
        "Inspection ID", "Client", "Location", "Frequency", "Scheduled", "Performed", "Price",
    ])
    table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    table.setMinimumHeight(300)
    by_id = {inspection.id: inspection for inspection in inspections}
    for row, inspection in enumerate(inspections):
        values = [
            (str(inspection.id), inspection.id),
            (inspection.client_name, inspection.client_name.casefold()),
            (inspection.location, inspection.location.casefold()),
            (inspection.frequency, inspection.frequency),
            (str(inspection.scheduled_date), inspection.scheduled_date.toordinal()),
            (str(inspection.performed_date) if inspection.performed_date else "Not Completed",
             inspection.performed_date.toordinal() if inspection.performed_date else 0),
            (f"${inspection.price:.2f}", inspection.price),
        ]
        for column, (label, value) in enumerate(values):
            item = SortableItem(label, value)
            item.setData(Qt.ItemDataRole.UserRole, inspection.id)
            table.setItem(row, column, item)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    table.setSortingEnabled(True)
    table.sortItems(0, Qt.SortOrder.AscendingOrder)
    table.cellClicked.connect(
        lambda row, column: on_open(by_id[table.item(row, column).data(Qt.ItemDataRole.UserRole)])
    )
    return table

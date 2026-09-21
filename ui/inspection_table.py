from nicegui import ui

from ui.inspection_dialog import show_inspection_details

ui.add_css("""
    .inspection-table thead th {
        border-right: 1px solid #d1d5db;
        font-weight: 600;
    }

    .inspection-table thead th:last-child {
        border-right: none;
    }

    .inspection-table tbody td {
        border-right: 1px solid #e5e7eb;
    }

    .inspection-table tbody td:last-child {
        border-right: none;
    }
""")

def show_inspection_table(inspections):

    ui.label(
        "All Inspections"
    ).classes("text-xl font-bold mt-6")



    columns = [
        {
            "name": "id",
            "label": "Inspection ID",
            "field": "id",
            "sortable": True,
            "align": "left",
        },
        {
            "name": "client_name",
            "label": "Client",
            "field": "client_name",
            "sortable": True,
        },
        {
            "name": "location",
            "label": "Location",
            "field": "location",
            "sortable": True,
        },
        {
            "name": "frequency",
            "label": "Frequency",
            "field": "frequency",
            "sortable": True,
        },
        {
            "name": "scheduled_date",
            "label": "Scheduled",
            "field": "scheduled_date",
            "sortable": True,
        },
        {
            "name": "performed_date",
            "label": "Performed",
            "field": "performed_date",
            "sortable": True,
        },
        {
            "name": "price",
            "label": "Price",
            "field": "price",
            "sortable": True,
        },
    ]

    rows = []

    for inspection in inspections:

        rows.append(
            {
                "id": inspection.id,
                "client_name": inspection.client_name,
                "location": inspection.location,
                "frequency": inspection.frequency,
                "scheduled_date": inspection.scheduled_date,
                "performed_date": (
                    inspection.performed_date
                    if inspection.performed_date
                    else "Not Completed"
                ),
                "price": f"${inspection.price:.2f}",
            }
        )

    table = ui.table(
        columns=columns,
        rows=rows,
        row_key="id",
        pagination=10,
    ).classes("inspection-table")

    def handle_row_click(e):

        row = e.args[1]

        inspection_id = row["id"]

        inspection = next(
            inspection
            for inspection in inspections
            if inspection.id == inspection_id
        )

        show_inspection_details(inspection, read_only=True)

    table.on(
        "rowClick",
        handle_row_click,
    )
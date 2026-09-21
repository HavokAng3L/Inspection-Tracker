from datetime import date, datetime

from nicegui import ui

from database import SessionLocal
from inspection_service import create_inspection


def show_add_inspection():

    with ui.dialog() as dialog, ui.card():

        ui.label(
            "Add New Inspection"
        ).classes("text-2xl font-bold")

        ui.separator()

        ui.label("Client Name")

        client_name_input = ui.input(
            placeholder="Enter client name"
        )

        ui.label("Location")

        location_input = ui.input(
            placeholder="Enter location"
        )

        ui.label("Frequency")

        frequency_input = ui.select(
            [
                "Annual",
                "Semi-Annual",
                "Quarterly",
            ],
            value="Annual",
        )

        ui.label("Start Date")

        start_date_input = ui.date(
            value=date.today()
        )

        ui.label("Scheduled Date")

        scheduled_date_input = ui.date(
            value=date.today()
        )

        ui.label("Price")

        price_input = ui.number(
            value=0,
            format="%.2f",
        )

        ui.label("Notes")

        notes_input = ui.textarea(
            placeholder="Optional notes"
        )

        ui.separator()

        def handle_create():

            if not client_name_input.value:

                ui.notify(
                    "Client name is required",
                    type="negative",
                )

                return

            if not location_input.value:

                ui.notify(
                    "Location is required",
                    type="negative",
                )

                return

            start_date = datetime.strptime(
                start_date_input.value,
                "%Y-%m-%d",
            ).date()

            scheduled_date = datetime.strptime(
                scheduled_date_input.value,
                "%Y-%m-%d",
            ).date()

            with SessionLocal() as session:

                create_inspection(
                    session=session,
                    client_name=client_name_input.value,
                    location=location_input.value,
                    frequency=frequency_input.value,
                    start_date=start_date,
                    scheduled_date=scheduled_date,
                    price=price_input.value,
                    notes=notes_input.value or None,
                )

            dialog.close()

            from ui.dashboard import dashboard
            dashboard.refresh()

            ui.notify(
                "Inspection Added"
            )

        with ui.row():

            ui.button(
                "Add Inspection",
                on_click=handle_create,
            )

            ui.button(
                "Cancel",
                on_click=dialog.close,
            )

    dialog.open()
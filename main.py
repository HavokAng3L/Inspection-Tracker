from datetime import date, datetime

from nicegui import ui

from database import engine, Base, SessionLocal
from models import Inspection

from inspection_service import (
    get_overdue_inspections,
    get_upcoming_inspections,
    get_due_soon_inspections,
    complete_inspection,
    update_inspection,
    delete_inspection, create_inspection,
    get_inspections
)


Base.metadata.create_all(engine)


def complete_inspection_ui(
    inspection,
    dialog,
    complete_button,
):
    complete_button.disable()

    with SessionLocal() as session:
        complete_inspection(
            session=session,
            inspection=inspection,
            performed_date=date.today(),
        )

    dialog.close()

    dashboard.refresh()

    ui.notify("Inspection Completed")


def show_inspection_details(inspection):

    with ui.dialog() as dialog, ui.card():

        ui.label(
            inspection.client_name
        ).classes("text-2xl font-bold")

        ui.separator()

        # Client Name
        ui.label("Client Name")

        client_name_input = ui.input(
            value=inspection.client_name
        )

        # Location
        ui.label("Location")

        location_input = ui.input(
            value=inspection.location
        )

        # Frequency
        ui.label("Frequency")

        frequency_input = ui.select(
            ["Annual", "Semi-Annual", "Quarterly"],
            value=inspection.frequency,
        )

        # Scheduled Date
        ui.label("Scheduled Date")

        scheduled_date_input = ui.date(
            value=inspection.scheduled_date
        )

        # Price
        ui.label("Price")

        price_input = ui.number(
            value=inspection.price,
            format="%.2f",
        )

        # Notes
        ui.label("Notes")

        notes_input = ui.textarea(
            value=inspection.notes or ""
        )

        ui.separator()

        def handle_save():

            with SessionLocal() as session:

                update_inspection(
                    session=session,
                    inspection=inspection,
                    client_name=client_name_input.value,
                    location=location_input.value,
                    frequency=frequency_input.value,
                    scheduled_date=scheduled_date_input.value,
                    price=price_input.value,
                    notes=notes_input.value or None,
                )

            dialog.close()

            dashboard.refresh()

            ui.notify("Inspection Updated")

        def handle_delete():

            with ui.dialog() as confirm_dialog, ui.card():

                ui.label(
                    "Delete this inspection?"
                ).classes("text-xl font-bold")

                ui.label(
                    "This cannot be undone."
                )

                with ui.row():

                    def confirm_delete():

                        with SessionLocal() as session:

                            inspection_db = session.get(
                                Inspection,
                                inspection.id,
                            )

                            if inspection_db is None:

                                ui.notify(
                                    "Inspection not found",
                                    type="negative",
                                )

                                confirm_dialog.close()

                                return

                            delete_inspection(
                                session=session,
                                inspection=inspection_db,
                            )

                        confirm_dialog.close()
                        dialog.close()

                        dashboard.refresh()

                        ui.notify(
                            "Inspection Deleted"
                        )

                    ui.button(
                        "Delete",
                        on_click=confirm_delete,
                    )

                    ui.button(
                        "Cancel",
                        on_click=confirm_dialog.close,
                    )

            confirm_dialog.open()

        with ui.row():

            ui.button(
                "Apply Changes",
                on_click=handle_save,
            )

            ui.button(
                "Cancel",
                on_click=dialog.close,
            )

            ui.button(
                "Delete Inspection",
                on_click=handle_delete,
            )

    dialog.open()


@ui.refreshable
def dashboard():

    with SessionLocal() as session:

        overdue_inspections = get_overdue_inspections(
            session
        )

        due_soon_inspections = get_due_soon_inspections(
            session
        )

        upcoming_inspections = get_upcoming_inspections(
            session
        )

        all_inspections = get_inspections(session)

    # Header

    ui.label(
        "Inspection Tracker (MINI)"
    ).classes("text-2xl font-bold")

    ui.label(
        "Welcome to V1 of Inspection Tracker (MINI)"
    )

    ui.button(
        "Add Inspection",
        on_click=show_add_inspection,
    ).classes("mt-4")

    # Dashboard counts

    with ui.row():

        with ui.card():

            ui.label("Overdue")

            ui.label(
                str(len(overdue_inspections))
            ).classes("text-3xl")

        with ui.card():

            ui.label("Due Soon")

            ui.label(
                str(len(due_soon_inspections))
            ).classes("text-3xl")

        with ui.card():

            ui.label("Upcoming")

            ui.label(
                str(len(upcoming_inspections))
            ).classes("text-3xl")

    # --------------------------------------------------
    # OVERDUE
    # --------------------------------------------------

    ui.label(
        "Overdue Inspections"
    ).classes("text-xl font-bold mt-6")

    for inspection in overdue_inspections:

        with ui.card().on(
            "click",
            lambda inspection=inspection:
                show_inspection_details(inspection),
        ):

            ui.label(
                inspection.client_name
            ).classes("text-lg font-bold")

            ui.label(
                f"Location: {inspection.location}"
            )

            ui.label(
                f"Scheduled: {inspection.scheduled_date}"
            )

            ui.label(
                f"Price: ${inspection.price:.2f}"
            )

    # --------------------------------------------------
    # DUE SOON
    # --------------------------------------------------

    ui.label(
        "Due Soon"
    ).classes("text-xl font-bold mt-6")

    for inspection in due_soon_inspections:

        with ui.card().on(
            "click",
            lambda inspection=inspection:
                show_inspection_details(inspection),
        ):

            ui.label(
                inspection.client_name
            ).classes("text-lg font-bold")

            ui.label(
                f"Location: {inspection.location}"
            )

            ui.label(
                f"Scheduled: {inspection.scheduled_date}"
            )

            ui.label(
                f"Price: ${inspection.price:.2f}"
            )

    # --------------------------------------------------
    # UPCOMING
    # --------------------------------------------------

    ui.label(
        "Upcoming"
    ).classes("text-xl font-bold mt-6")

    for inspection in upcoming_inspections:

        with ui.card().on(
            "click",
            lambda inspection=inspection:
                show_inspection_details(inspection),
        ):

            ui.label(
                inspection.client_name
            ).classes("text-lg font-bold")

            ui.label(
                f"Location: {inspection.location}"
            )

            ui.label(
                f"Scheduled: {inspection.scheduled_date}"
            )

            ui.label(
                f"Price: ${inspection.price:.2f}"
            )

    # --------------------------------------------------
    # ALL INSPECTIONS
    # --------------------------------------------------

    ui.label(
        "All Inspections"
    ).classes("text-xl font-bold mt-6")

    columns = [
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

    for inspection in all_inspections:
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
    )

    table.on(
        "rowClick",
        lambda e: show_inspection_details(
            next(
                inspection
                for inspection in all_inspections
                if inspection.id == e.args["row"]["id"]
            )
        ),
    )

    
def show_add_inspection():

    with ui.dialog() as dialog, ui.card():

        ui.label(
            "Add New Inspection"
        ).classes("text-2xl font-bold")

        ui.separator()

        # Client Name
        ui.label("Client Name")

        client_name_input = ui.input(
            placeholder="Enter client name"
        )

        # Location
        ui.label("Location")

        location_input = ui.input(
            placeholder="Enter location"
        )

        # Frequency
        ui.label("Frequency")

        frequency_input = ui.select(
            ["Annual", "Semi-Annual", "Quarterly"],
            value="Annual",
        )

        # Start Date
        ui.label("Start Date")

        start_date_input = ui.date(
            value=date.today()
        )

        # Scheduled Date
        ui.label("Scheduled Date")

        scheduled_date_input = ui.date(
            value=date.today()
        )

        # Price
        ui.label("Price")

        price_input = ui.number(
            value=0,
            format="%.2f",
        )

        # Notes
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

            with SessionLocal() as session:

                start_date = start_date_input.value
                scheduled_date = scheduled_date_input.value

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

dashboard()

ui.run()
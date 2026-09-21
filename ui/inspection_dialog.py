from datetime import date

from nicegui import ui

from database import SessionLocal
from models import Inspection

from inspection_service import (
    complete_inspection,
    update_inspection,
    delete_inspection,
)


def show_inspection_details(inspection, read_only=False):

    with ui.dialog() as dialog, ui.card():

        ui.label(
            inspection.client_name
        ).classes("text-2xl font-bold")

        ui.separator()

        ui.label("Client Name")

        client_name_input = ui.input(
            value=inspection.client_name
        )

        ui.label("Location")

        location_input = ui.input(
            value=inspection.location
        )

        ui.label("Frequency")

        frequency_input = ui.select(
            [
                "Annual",
                "Semi-Annual",
                "Quarterly",
            ],
            value=inspection.frequency,
        )

        ui.label("Scheduled Date")

        scheduled_date_input = ui.date(
            value=inspection.scheduled_date
        )

        ui.label("Price")

        price_input = ui.number(
            value=inspection.price,
            format="%.2f",
        )

        ui.label("Notes")

        notes_input = ui.textarea(
            value=inspection.notes or ""
        )

        # ---------------------------------------------------------
        # Read-only mode
        # ---------------------------------------------------------

        if read_only:

            client_name_input.disable()
            location_input.disable()
            frequency_input.disable()
            scheduled_date_input.disable()
            price_input.disable()
            notes_input.disable()

            ui.separator()

            ui.button(
                "Close",
                on_click=dialog.close,
            )

        # ---------------------------------------------------------
        # Editable mode
        # ---------------------------------------------------------

        else:

            ui.separator()

            def handle_complete():

                complete_button.disable()

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

                        complete_button.enable()

                        return

                    complete_inspection(
                        session=session,
                        inspection=inspection_db,
                        performed_date=date.today(),
                    )

                dialog.close()

                from ui.dashboard import dashboard
                dashboard.refresh()

                ui.notify(
                    "Inspection Completed"
                )

            def handle_save():

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

                        return

                    update_inspection(
                        session=session,
                        inspection=inspection_db,
                        client_name=client_name_input.value,
                        location=location_input.value,
                        frequency=frequency_input.value,
                        scheduled_date=scheduled_date_input.value,
                        price=price_input.value,
                        notes=notes_input.value or None,
                    )

                dialog.close()

                from ui.dashboard import dashboard
                dashboard.refresh()

                ui.notify(
                    "Inspection Updated"
                )

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

                            from ui.dashboard import dashboard
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

                complete_button = ui.button(
                    "Complete Inspection",
                    on_click=handle_complete,
                ).props(
                    "color=positive"
                ).classes(
                    "font-bold"
                )

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
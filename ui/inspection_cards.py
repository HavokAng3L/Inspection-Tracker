from nicegui import ui

from ui.inspection_dialog import show_inspection_details


def show_inspection_section(title, inspections):

    ui.label(
        title
    ).classes("text-xl font-bold mt-6")

    for inspection in inspections:

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
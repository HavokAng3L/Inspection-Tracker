from nicegui import ui

from database import SessionLocal

from inspection_service import (
    get_overdue_inspections,
    get_due_soon_inspections,
    get_upcoming_inspections,
    get_inspections,
)

from ui.inspection_cards import show_inspection_section
from ui.inspection_table import show_inspection_table
from ui.inspection_form import show_add_inspection


@ui.refreshable
def dashboard():

    with SessionLocal() as session:

        overdue_inspections = get_overdue_inspections(session)

        due_soon_inspections = get_due_soon_inspections(session)

        upcoming_inspections = get_upcoming_inspections(session)

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

    # Counts

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

    # Inspection sections

    show_inspection_section(
        "Overdue Inspections",
        overdue_inspections,
    )

    show_inspection_section(
        "Due Soon",
        due_soon_inspections,
    )

    show_inspection_section(
        "Upcoming",
        upcoming_inspections,
    )

    # All inspections

    show_inspection_table(all_inspections)
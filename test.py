from database import engine, Base, SessionLocal
from inspection_service import (
    get_overdue_inspections,
    get_upcoming_inspections,
    get_due_soon_inspections,
    get_inspections,
    complete_inspection,
    update_inspection,
    delete_inspection,
    create_inspection,
)

Base.metadata.create_all(engine)


with SessionLocal() as session:

    print("\nALL INSPECTIONS")
    print("----------------")

    for inspection in get_inspections(session):
        print(
            f"ID: {inspection.id} | "
            f"{inspection.client_name} | "
            f"Scheduled: {inspection.scheduled_date} | "
            f"Performed: {inspection.performed_date}"
        )

    print("\nCOUNTS")
    print("----------------")
    print("Overdue:", len(get_overdue_inspections(session)))
    print("Due Soon:", len(get_due_soon_inspections(session)))
    print("Upcoming:", len(get_upcoming_inspections(session)))
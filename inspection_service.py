from datetime import date, timedelta

from sqlalchemy.orm import Session

from models import Inspection
from scheduling import get_next_scheduled_date

# This function deletes the record from the database
def delete_inspection(
        session: Session,
        inspection: Inspection
) -> None:
    session.delete(inspection)
    session.commit()

# This function updates the database record.
# Updating Inspections
def update_inspection(
    session: Session,
    inspection: Inspection,
    client_name: str,
    location: str,
    frequency: str,
    scheduled_date: date,
    price: float,
    notes: str | None = None,
) -> Inspection:

    inspection = session.get(
        Inspection,
        inspection.id
    )

    if inspection is None:
        raise ValueError("Inspection not found")

    inspection.client_name = client_name
    inspection.location = location
    inspection.frequency = frequency
    inspection.scheduled_date = scheduled_date
    inspection.price = price
    inspection.notes = notes

    session.commit()
    session.refresh(inspection)

    return inspection

# Creates a new record and pushes it to the database
# Creating Inspections
def create_inspection(
        session: Session,
        client_name: str,
        location: str,
        frequency: str,
        start_date: date,
        scheduled_date: date,
        price: float,
        notes: str | None = None,
) -> Inspection:

    new_inspection = Inspection(
        client_name=client_name,
        location=location,
        frequency=frequency,
        start_date=start_date,
        scheduled_date=scheduled_date,
        price=price,
        notes=notes,
    )

    session.add(new_inspection)
    session.commit()
    session.refresh(new_inspection)

    return new_inspection

# Retrieving One Inspection by ID
def get_inspection(
        session:Session,
        inspection_id: int
) -> Inspection | None:
    return session.get(Inspection, inspection_id)

# Creating Complete Inspection and Adding to DB
def complete_inspection(
    session: Session,
    inspection: Inspection,
    performed_date: date
) -> Inspection:

    inspection = session.get(Inspection, inspection.id)

    if inspection is None:
        raise ValueError("Inspection not found")

    inspection.performed_date = performed_date

    next_scheduled_date = get_next_scheduled_date(
        inspection.start_date,
        inspection.frequency,
        inspection.scheduled_date,
    )

    next_inspection = Inspection(
        client_name=inspection.client_name,
        location=inspection.location,
        frequency=inspection.frequency,
        start_date=inspection.start_date,
        scheduled_date=next_scheduled_date,
        price=inspection.price,
        notes=None,
    )

    session.add(next_inspection)
    session.commit()

    return next_inspection


# Gets ALL Inspections
def get_inspections(session: Session) -> list[Inspection]:
    return session.query(Inspection).all()

def get_upcoming_inspections(
        session: Session,
        days: int = 30,
) -> list[Inspection]:

    today = date.today()
    start_date = today + timedelta(days=7)
    end_date = today  + timedelta(days=days)

    return (
        session.query(Inspection)
        .filter(
    Inspection.performed_date.is_(None),
            Inspection.scheduled_date > start_date,
            Inspection.scheduled_date <= end_date,
        )
        .order_by(Inspection.scheduled_date)
        .all()
    )

def get_overdue_inspections(
        session: Session,
) -> list[Inspection]:
    today = date.today()

    return (
        session.query(Inspection)
        .filter(
            Inspection.performed_date.is_(None),
            Inspection.scheduled_date < today,
        )
        .order_by(Inspection.scheduled_date)
        .all()
    )

def get_due_soon_inspections(
    session: Session,
) -> list[Inspection]:

    today = date.today()
    end_date = today + timedelta(days=7)

    return(
        session.query(Inspection)
        .filter(
            Inspection.performed_date.is_(None),
            Inspection.scheduled_date > today,
            Inspection.scheduled_date <= end_date,
        )
        .order_by(Inspection.scheduled_date)
        .all()
    )
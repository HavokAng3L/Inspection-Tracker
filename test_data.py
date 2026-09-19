from datetime import date, timedelta

from database import engine, Base, SessionLocal
from inspection_service import create_inspection


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


today = date.today()


with SessionLocal() as session:

    # OVERDUE
    create_inspection(
        session=session,
        client_name="Overdue Company",
        location="100 Old Street",
        frequency="Quarterly",
        start_date=today - timedelta(days=90),
        scheduled_date=today - timedelta(days=10),
        price=100.00,
        notes="Test overdue inspection",
    )

    # DUE SOON
    create_inspection(
        session=session,
        client_name="Due Soon Company",
        location="200 Soon Street",
        frequency="Quarterly",
        start_date=today,
        scheduled_date=today + timedelta(days=3),
        price=200.00,
        notes="Test due soon inspection",
    )

    # DUE SOON
    create_inspection(
        session=session,
        client_name="Another Soon Company",
        location="300 Soon Street",
        frequency="Annual",
        start_date=today,
        scheduled_date=today + timedelta(days=7),
        price=300.00,
        notes="Test due soon inspection",
    )

    # UPCOMING
    create_inspection(
        session=session,
        client_name="Upcoming Company",
        location="400 Future Street",
        frequency="Semi-Annual",
        start_date=today,
        scheduled_date=today + timedelta(days=15),
        price=400.00,
        notes="Test upcoming inspection",
    )

    # UPCOMING
    create_inspection(
        session=session,
        client_name="Another Upcoming Company",
        location="500 Future Street",
        frequency="Annual",
        start_date=today,
        scheduled_date=today + timedelta(days=30),
        price=500.00,
        notes="Test upcoming inspection",
    )

    print("Test data created.")
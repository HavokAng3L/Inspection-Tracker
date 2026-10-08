import os
from pathlib import Path

from sqlalchemy import URL, create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def database_path() -> Path:
    """Keep mutable data outside the executable and its extraction directory."""
    override = os.environ.get("INSPECTION_TRACKER_DB")
    if override:
        return Path(override).expanduser().resolve()
    if os.name == "nt":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return root / "InspectionTracker" / "inspections.db"


DATABASE_PATH = database_path()
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
engine = create_engine(
    URL.create("sqlite", database=str(DATABASE_PATH)),
    connect_args={"timeout": 5},
)


@event.listens_for(engine, "connect")
def configure_sqlite(connection, _record):
    cursor = connection.cursor()
    try:
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA busy_timeout=5000")
    finally:
        cursor.close()


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine)

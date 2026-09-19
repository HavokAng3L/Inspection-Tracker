from datetime import date

from sqlalchemy import Date, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

# This class is created as a data representation of a
# Inspection.
class Inspection(Base):
    __tablename__ = "inspections"

    id: Mapped[int] = mapped_column(primary_key=True)

    client_name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)

    frequency: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)

    scheduled_date: Mapped[date] = mapped_column(Date, nullable=False)
    performed_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    price: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
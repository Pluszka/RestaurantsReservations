from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

class ReservationStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

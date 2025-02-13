from dbapplication.models import BaseModel, db


class Manager(BaseModel):
    __tablename__ = 'manager'
    name = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    city = db.Column(db.String(45), nullable=False)

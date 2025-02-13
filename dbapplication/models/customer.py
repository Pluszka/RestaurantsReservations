from dbapplication.models import BaseModel, db


class Customer(BaseModel):
    __tablename__ = 'customer'
    name = db.Column(db.String(45), unique=True, nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    discount = db.Column(db.Integer, nullable=True)

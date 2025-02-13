from dbapplication.models import BaseModel, db


class Restaurant(BaseModel):
    __tablename__ = 'restaurant'
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False)
    manager = db.relationship('Manager')
    name = db.Column(db.String(45), nullable=False)
    city = db.Column(db.String(45), nullable=False)
    total_guest_number = db.Column(db.Integer, nullable=False)



from dbapplication.models import BaseModel, db




class Reservation(BaseModel):
    __tablename__ = 'reservation'
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    restaurant = db.relationship('Restaurant')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
    customer = db.relationship('Customer')
    partner_company_id = db.Column(db.Integer, db.ForeignKey('partner_company.id'), nullable=True)
    partner_company = db.relationship('PartnerCompany')
    date = db.Column(db.DateTime, nullable=False)
    reservation_name = db.Column(db.String(45), nullable=False)
    guest_number = db.Column(db.Integer, nullable=False)
    allergies = db.Column(db.String(120), nullable=True)
    total_cost = db.Column(db.Float, nullable=False)
    reservation_status = db.Column(db.String(20), nullable=False)


from dbapplication.models import BaseModel, db


class PartnerCompany(BaseModel):
    __tablename__ = 'partner_company'
    name = db.Column(db.String(45), unique=True, nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    discount = db.Column(db.Integer, nullable=True)

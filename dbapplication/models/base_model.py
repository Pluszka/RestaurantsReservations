from dbapplication.app import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

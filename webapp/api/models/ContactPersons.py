import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class ContactPerson(db.Model):
    __tablename__ = "contactpersons"
    idcontactperson = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(50))
    nomorwa = db.Column(db.String(15))
    is_active = db.Column(db.Boolean(), default=0)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    user_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    # relationship

    def __init__(self, nama, nomorwa, is_active):
        self.nama = nama
        self.nomorwa = nomorwa
        self.is_active = is_active

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class ContactPersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ContactPerson
        sqla_session = db.session

    idcontactperson = fields.Integer(dump_only=True)
    nama = fields.String(required=True)
    nomorwa = fields.String(required=True)
    is_active = fields.Boolean()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    user_id = fields.Integer()

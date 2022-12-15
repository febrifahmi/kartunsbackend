import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Member(db.Model):
    __tablename__ = "members"
    idmember = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomoranggota = db.Column(db.String(50))
    validfrom = db.Column(db.String(8))
    validthru = db.Column(db.String(8))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    user_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    # relationship

    def __init__(
        self, nomoranggota, validfrom, validthru
    ):
        self.nomoranggota = nomoranggota
        self.validfrom = validfrom
        self.validthru = validthru

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member
        sqla_session = db.session

    idmember = fields.Integer(dump_only=True)
    nomoranggota = fields.String(required=True)
    validfrom = fields.String(required=True)
    validthru = fields.String(required=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    user_id = fields.Integer()
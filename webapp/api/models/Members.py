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
    alamat = db.Column(db.String(80))
    notelp = db.Column(db.String(20))
    pekerjaan = db.Column(db.String(20))
    perusahaan = db.Column(db.String(50))
    kantor = db.Column(db.String(50))
    alamatkantor = db.Column(db.String(50))
    mulaibekerja = db.Column(db.String(10))
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
    alamat = fields.String()
    notelp = fields.String()
    pekerjaan = fields.String()
    perusahaan = fields.String()
    kantor = fields.String()
    alamatkantor = fields.String()
    mulaibekerja = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    user_id = fields.Integer()
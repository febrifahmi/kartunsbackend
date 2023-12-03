import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class IuranMember(db.Model):
    __tablename__ = "iuranmembers"
    idiuran = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomoranggota = db.Column(db.String(50))
    namaanggota = db.Column(db.String(80))
    tahun = db.Column(db.String(4))
    jumlahiuran = db.Column(db.Integer, default=0)
    bankpengirim = db.Column(db.String(80))
    iuranimgurl = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    member_id = db.Column(db.Integer, db.ForeignKey("members.idmember"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    # relationship

    def __init__(
        self,
        nomoranggota,
        namaanggota,
        tahun,
        jumlahiuran,
        bankpengirim,
        iuranimgurl,
        member_id,
        user_id,
        file,
    ):
        self.nomoranggota = nomoranggota
        self.namaanggota = namaanggota
        self.tahun = tahun
        self.jumlahiuran = jumlahiuran
        self.bankpengirim = bankpengirim
        self.iuranimgurl = iuranimgurl
        self.member_id = member_id
        self.user_id = user_id
        self.file = file

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class IuranMemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IuranMember
        sqla_session = db.session

    idiuran = fields.Integer(dump_only=True)
    nomoranggota = fields.String(required=True)
    namaanggota = fields.String(required=True)
    tahun = fields.String(required=True)
    jumlahiuran = fields.Integer(required=True)
    bankpengirim = fields.String(required=True)
    iuranimgurl = fields.String(required=True)
    file = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    member_id = fields.Integer()
    user_id = fields.Integer()

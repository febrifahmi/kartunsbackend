import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields

class Donations(db.Model):
    __tablename__ = "donations"
    iddonation = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namadonatur = db.Column(db.String(50))
    bankpengirim = db.Column(db.String(50))
    jumlahdonasi = db.Column(db.Integer)
    rektujuan = db.Column(db.String(50))
    donasiimgurl = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    donatur_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    def __init__(
        self, namadonatur, bankpengirim, jumlahdonasi, rektujuan, donasiimgurl, donatur_id, file
    ):
        self.namadonatur = namadonatur
        self.bankpengirim = bankpengirim
        self.jumlahdonasi = jumlahdonasi
        self.rektujuan = rektujuan
        self.donasiimgurl = donasiimgurl
        self.donatur_id = donatur_id
        self.file = file

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    

class DonationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Donations
        sqla_session = db.session

    iddonation = fields.Integer(dump_only=True)
    namadonatur = fields.String(required=True)
    bankpengirim = fields.String(required=True)
    jumlahdonasi = fields.Integer(required=True)
    rektujuan = fields.String(required=True)
    donasiimgurl = fields.String(required=True)
    file = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    donatur_id = fields.Integer()
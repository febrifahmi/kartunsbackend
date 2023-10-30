# tanggal
# judul/deskripsi
# type (income/spending)
# kategori (gaji, transport, sumbangan, dsb)
# jumlah

import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields

class AnggaranArusKas(db.Model):
    __tablename__ = "kas"
    idaruskas = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aruskastitle = db.Column(db.String(50))
    aruskasdesc = db.Column(db.String(140))
    aruskasmonth = db.Column(db.String(20))
    aruskasyear = db.Column(db.String(10))
    filekasuri = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk

    # relationship

    def __init__(
        self, aruskastitle, aruskasdesc, aruskasmonth, aruskasyear, filekasuri, file
    ):
        self.aruskastitle = aruskastitle
        self.aruskasdesc = aruskasdesc
        self.aruskasmonth = aruskasmonth
        self.aruskasyear = aruskasyear
        self.filekasuri = filekasuri
        self.file = file

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class AnggaranArusKasSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AnggaranArusKas
        sqla_session = db.session

    idaruskas = fields.Integer(dump_only=True)
    aruskastitle = fields.String(required=True)
    aruskasdesc = fields.String(required=True)
    aruskasmonth = fields.String(required=True)
    aruskasyear = fields.String(required=True)
    filekasuri = fields.String()
    file = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
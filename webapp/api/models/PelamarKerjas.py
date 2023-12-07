import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class PelamarKerja(db.Model):
    __tablename__ = "pelamarkerjas"
    idpelamar = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namapelamar = db.Column(db.String(80))
    doksuratlamaran = db.Column(db.String(128))
    dokcv = db.Column(db.String(128))
    dokportofolio = db.Column(db.String(128))
    hasilseleksiakhir = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    joboffer_id = db.Column(db.Integer, db.ForeignKey("joboffers.idoffer"))
    pelamar_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    def __init__(
        self,
        namapelamar,
        doksuratlamaran,
        dokcv,
        dokportofolio,
        joboffer_id,
        pelamar_id,
    ):
        self.namapelamar = namapelamar
        self.doksuratlamaran = doksuratlamaran
        self.dokcv = dokcv
        self.dokportofolio = dokportofolio
        self.joboffer_id = joboffer_id
        self.pelamar_id = pelamar_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class PelamarKerjaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PelamarKerja
        sqla_session = db.session

    idpelamar = fields.Integer(dump_only=True)
    namapelamar = fields.String(required=True)
    doksuratlamaran = fields.String(required=True)
    dokcv = fields.String(required=True)
    dokportofolio = fields.String(required=True)
    hasilseleksiakhir = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    joboffer_id = fields.Integer(required=True)
    pelamar_id = fields.Integer(required=True)

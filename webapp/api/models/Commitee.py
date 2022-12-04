# Data pengurus KartUNS mulai dari ketua sampai pengurus biasa
# model ini diperlukan untuk bisa mengupdate susunan kepengurusan, data digunakan pada letter
# sertifikat, dan dokumen organisasi lainnya.

import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Pengurus(db.Model):
    __tablename__ = "pengurus"
    idpengurus = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namapengurus = db.Column(db.String(50))
    jabatan = db.Column(db.String(50))
    tahunkepengurusan = db.Column(db.String(6))
    tanggalmulai = db.Column(db.String(8))
    tanggalselesai = db.Column(db.String(8))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    pengurus_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    def __init__(
        self, namapengurus, jabatan, tahunkepengurusan, tanggalmulai, tanggalselesai
    ):
        self.namapengurus = namapengurus
        self.jabatan = jabatan
        self.tahunkepengurusan = tahunkepengurusan
        self.tanggalmulai = tanggalmulai
        self.tanggalselesai = tanggalselesai

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class PengurusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pengurus
        sqla_session = db.session

    idpengurus = fields.Integer(dump_only=True)
    namapengurus = fields.String(required=True)
    jabatan = fields.String(required=True)
    tahunkepengurusan = fields.String()
    tanggalmulai = fields.String(required=True)
    tanggalselesai = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    advertiser_id = fields.Integer()
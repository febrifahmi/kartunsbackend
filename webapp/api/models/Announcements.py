import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Pengumuman(db.Model):
    __tablename__ = "pengumuman"
    idpengumuman = db.Column(db.Integer, primary_key=True, autoincrement=True)
    judul = db.Column(db.String(80))
    pengumumanimgurl = db.Column(db.String(128))
    pengumumandesc = db.Column(db.String(140))
    pengumumantext = db.Column(db.String(500))
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)

    # fk

    # relationship

    def __init__(
        self, judul, pengumumanimgurl, pengumumandesc, pengumumantext,
    ):
        self.judul = judul
        self.pengumumanimgurl = pengumumanimgurl
        self.pengumumandesc = pengumumandesc
        self.pengumumantext = pengumumantext

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class PengumumanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pengumuman
        sqla_session = db.session

    idpengumuman = fields.Integer(dump_only=True)
    judul = fields.String(required=True)
    pengumumanimgurl = fields.String(required=True)
    pengumumandesc = fields.String()
    pengumumantext = fields.String(required=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
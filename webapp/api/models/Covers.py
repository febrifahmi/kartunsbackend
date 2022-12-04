# cover digunakan untuk menampilkan pengumuman-pengumuman sangat penting/perlu highlight
# dalam bentuk caraousel di home page

import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Cover(db.Model):
    __tablename__ = "covers"
    idcover = db.Column(db.Integer, primary_key=True, autoincrement=True)
    covertitle = db.Column(db.String(50))
    coverimgurl = db.Column(db.String(128))
    coverdesc = db.Column(db.String(140))
    covertext = db.Column(db.String(800))
    nrdaysserved = db.Column(db.Integer, default=3)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk

    def __init__(
        self, covertitle, coverimgurl, coverdesc, covertext, nrdaysserved,
    ):
        self.covertitle = covertitle
        self.coverimgurl = coverimgurl
        self.coverdesc = coverdesc
        self.covertext = covertext
        self.nrdaysserved = nrdaysserved

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class CoverSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cover
        sqla_session = db.session

    idcover = fields.Integer(dump_only=True)
    covertitle = fields.String(required=True)
    coverimgurl = fields.String(required=True)
    coverdesc = fields.String()
    covertext = fields.String(required=True)
    nrdaysserved = fields.Integer()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields
from webapp.api.models.Users import UserSchema


class SuratMasuk(db.Model):
    __tablename__ = "suratmasuks"
    idsuratmasuk = db.Column(db.Integer, primary_key=True, autoincrement=True)
    suratmasuktitle = db.Column(db.String(50))
    suratmasuknr = db.Column(db.String(20))
    filesurat = db.Column(db.String(128))
    suratmasukdesc = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk

    def __init__(
        self, suratmasuktitle, suratmasuknr, suratmasukdesc, filesurat
    ):
        self.suratmasuktitle = suratmasuktitle
        self.suratmasuknr = suratmasuknr
        self.suratmasukdesc = suratmasukdesc
        self.filesurat = filesurat
    

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class SuratMasukSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SuratMasuk
        sqla_session = db.session

    idsuratmasuk = fields.Integer(dump_only=True)
    suratmasuktitle = fields.String(required=True)
    suratmasuknr = fields.String(required=True)
    filesurat = fields.String()
    suratmasukdesc = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
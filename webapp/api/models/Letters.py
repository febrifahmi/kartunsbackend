import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields
from webapp.api.models.Users import UserSchema


class Letter(db.Model):
    __tablename__ = "letters"
    idsuratkeluar = db.Column(db.Integer, primary_key=True, autoincrement=True)
    suratkeluartitle = db.Column(db.String(50))
    suratkeluarnr = db.Column(db.String(20))
    suratkeluardesc = db.Column(db.String(140))
    kepada = db.Column(db.String(128))
    filesuratkeluaruri = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk

    def __init__(
        self,
        suratkeluartitle,
        suratkeluarnr,
        suratkeluardesc,
        kepada,
        filesuratkeluaruri,
        file,
    ):
        self.suratkeluartitle = suratkeluartitle
        self.suratkeluarnr = suratkeluarnr
        self.suratkeluardesc = suratkeluardesc
        self.kepada = kepada
        self.filesuratkeluaruri = filesuratkeluaruri
        self.file = file

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class LetterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Letter
        sqla_session = db.session

    idsuratkeluar = fields.Integer(dump_only=True)
    suratkeluartitle = fields.String(required=True)
    suratkeluarnr = fields.String(required=True)
    suratkeluardesc = fields.String()
    kepada = fields.String()
    filesuratkeluaruri = fields.String()
    file = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)

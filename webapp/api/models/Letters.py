import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields
from webapp.api.models.Users import UserSchema


class Letter(db.Model):
    __tablename__ = "letters"
    idletter = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lettertitle = db.Column(db.String(50))
    letternr = db.Column(db.String(20))
    qrcodestring = db.Column(db.String(128))
    letterdesc = db.Column(db.String(140))
    lettertext = db.Column(db.String(1500))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    penandatangan_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    def __init__(
        self, lettertitle, letternr, letterdesc, lettertext,
    ):
        self.lettertitle = lettertitle
        self.letternr = letternr
        self.letterdesc = letterdesc
        self.lettertext = lettertext
    
    def setQRcodeString(self, kode):
        self.qrcodestring = "{}".format(kode)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class LetterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Letter
        sqla_session = db.session

    idletter = fields.Integer(dump_only=True)
    lettertitle = fields.String(required=True)
    letternr = fields.String(required=True)
    qrcodestring = fields.String()
    letterdesc = fields.String()
    lettertext = fields.String(required=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    penandatangan_id = fields.Integer()
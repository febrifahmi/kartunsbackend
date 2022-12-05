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
    signimgurl = db.Column(db.String(128))
    letterdesc = db.Column(db.String(140))
    lettertext = db.Column(db.String(1500))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk

    # relationship
    penandatangan = db.relationship("User", backref="Penandatangan", cascade="all, delete-orphan")

    def __init__(
        self, lettertitle, signimgurl, letterdesc, lettertext,
    ):
        self.lettertitle = lettertitle
        self.signimgurl = signimgurl
        self.letterdesc = letterdesc
        self.lettertext = lettertext

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
    signimgurl = fields.String(required=True)
    letterdesc = fields.String()
    lettertext = fields.String(required=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    penandatangan = fields.Nested(
        UserSchema,
        many=True,
        only=["iduser","username", "first_name", "last_name"],
    )
import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields
from webapp.api.models.Users import UserSchema


class Scholarship(db.Model):
    __tablename__ = "scholarships"
    idbeasiswa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    beasiswatitle = db.Column(db.String(150))
    beasiswaimgurl = db.Column(db.String(128))
    beasiswadesc = db.Column(db.String(140))
    beasiswatext = db.Column(db.String(800))
    is_active = db.Column(db.Boolean(), default=0)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    author_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    # relationship
    penerimabeasiswa = db.relationship(
        "User", backref="penerimabeasiswa", lazy="dynamic"
    )

    def __init__(
        self, beasiswatitle, beasiswaimgurl, beasiswadesc, beasiswatext, is_active, file
    ):
        self.beasiswatitle = beasiswatitle
        self.beasiswaimgurl = beasiswaimgurl
        self.beasiswadesc = beasiswadesc
        self.beasiswatext = beasiswatext
        self.is_active = is_active
        self.file = file

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class ScholarshipSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Scholarship
        sqla_session = db.session

    idbeasiswa = fields.Integer(dump_only=True)
    beasiswatitle = fields.String(required=True)
    beasiswaimgurl = fields.String()
    beasiswadesc = fields.String(required=True)
    beasiswatext = fields.String(required=True)
    is_active = fields.Boolean()
    file = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    author_id = fields.Integer()
    penerimabeasiswa = fields.Nested(
        UserSchema, many=True, only=["iduser", "username", "first_name", "last_name"]
    )

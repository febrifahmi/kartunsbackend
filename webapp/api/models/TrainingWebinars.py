import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class TrainingWebinar(db.Model):
    __tablename__ = "trainingwebinars"
    idwebinar = db.Column(db.Integer, primary_key=True, autoincrement=True)
    webinartitle = db.Column(db.String(50))
    webinarimgurl = db.Column(db.String(128))
    webinardesc = db.Column(db.String(140))
    webinartext = db.Column(db.String(1500))
    startdate = db.Column(db.String(10))
    enddate = db.Column(db.String(10))
    level = db.Column(db.String(20))
    price = db.Column(db.Integer)
    is_verified = db.Column(db.Boolean(), default=0)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    author_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    def __init__(
        self,
        webinartitle,
        webinarimgurl,
        webinardesc,
        webinartext,
        startdate,
        enddate,
        level,
        price,
        file
    ):
        self.webinartitle = webinartitle
        self.webinarimgurl = webinarimgurl
        self.webinardesc = webinardesc
        self.webinartext = webinartext
        self.startdate = startdate
        self.enddate = enddate
        self.level = level
        self.price = price
        self.file = file

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class TrainingWebinarSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainingWebinar
        sqla_session = db.session

    idwebinar = fields.Integer(dump_only=True)
    webinartitle = fields.String(required=True)
    webinarimgurl = fields.String(required=True)
    webinardesc = fields.String(required=True)
    webinartext = fields.String(required=True)
    startdate = fields.String(required=True)
    enddate = fields.String(required=True)
    level = fields.String()
    price = fields.Integer()
    file = fields.String()
    is_verified = db.Column(db.Boolean(), default=0)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    author_id = fields.Integer()

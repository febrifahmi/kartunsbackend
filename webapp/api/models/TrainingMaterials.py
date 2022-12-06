import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class TrainingMaterial(db.Model):
    __tablename__ = "trainingmaterials"
    idtm = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tmtitle = db.Column(db.String(50))
    tmimgurl = db.Column(db.String(128))
    tmdesc = db.Column(db.String(140))
    tmtext = db.Column(db.String(800))
    urifile = db.Column(db.String)
    is_verified = db.Column(db.Boolean(), default=0)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.idtraining"))

    def __init__(
        self, tmtitle, tmimgurl, tmdesc, tmtext, urifile, startdate, level, price
    ):
        self.tmtitle = tmtitle
        self.tmimgurl = tmimgurl
        self.tmdesc = tmdesc
        self.tmtext = tmtext
        self.startdate = startdate
        self.urifile = urifile
        self.level = level
        self.price = price

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class TrainMatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainingMaterial
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    tmtitle = fields.String(required=True)
    tmimgurl = fields.String(required=True)
    tmdesc = fields.String()
    tmtext = fields.String(required=True) 
    urifile = fields.Integer()
    is_verified = fields.Boolean()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    training_id = fields.Integer()
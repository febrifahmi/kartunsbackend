# training dapat dibeli/disubscribe
# training sekaligus sbg kelas. semua user yg pernah membeli training otomatis berada dalam kelas
# training dilaksanakan melalui sistem online/webinar atau offline/luring
# training dapat berisi banyak materials, namun pembelajaran, test dan penilaian tidak dilaksanakan dalam
# website/dilaksanakan masing-masing pemateri melalui program training masing-masing

import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Training(db.Model):
    __tablename__ = "trainings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trainingtitle = db.Column(db.String(50))
    trainingimgurl = db.Column(db.String(128))
    trainingdesc = db.Column(db.String(140))
    trainingtext = db.Column(db.String(800))
    durationday = db.Column(db.Integer)
    startdate = db.Column(db.Integer, default=8)
    level = db.Column(db.String(20))
    price = db.Column(db.Integer)
    is_verified = db.Column(db.Boolean(), default=0)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    trainer_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    def __init__(
        self,
        trainingtitle,
        trainingimgurl,
        trainingdesc,
        trainingtext,
        durationday,
        level,
        price,
    ):
        self.trainingtitle = trainingtitle
        self.trainingimgurl = trainingimgurl
        self.trainingdesc = trainingdesc
        self.trainingtext = trainingtext
        self.durationday = durationday
        self.level = level
        self.price = price

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class TrainingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Training
        sqla_session = db.session

    idtraining = fields.Integer(dump_only=True)
    trainingtitle = fields.String(required=True)
    trainingimgurl = fields.String(required=True)
    trainingdesc = fields.String()
    trainingtext = fields.String(required=True)
    durationday = fields.Integer()
    startdate = fields.Integer()
    level = fields.String()
    price = fields.Integer()
    is_verified = db.Column(db.Boolean(), default=0)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    trainer_id = fields.Integer()

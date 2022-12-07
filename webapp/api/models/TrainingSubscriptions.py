import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class TrainingSubscription(db.Model):
    __tablename__ = "trainingsubscription"
    idtsub = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tsubsnumber = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    subscriber_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.idtraining"))

    def __init__(
        self,
        tsubsnumber
    ):
        self.tsubsnumber = tsubsnumber

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class TsubsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainingSubscription
        sqla_session = db.session

    idtsub = fields.Integer(dump_only=True)
    tsubnumber = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    subscriber_id = fields.Integer()
    training_id = fields.Integer()
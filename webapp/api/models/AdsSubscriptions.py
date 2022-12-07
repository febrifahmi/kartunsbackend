import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class AdSubscription(db.Model):
    __tablename__ = "adsubscription"
    idadsub = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adsubnumber = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    subscriber_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))
    ad_id = db.Column(db.Integer, db.ForeignKey("ads.idad"))

    def __init__(
        self,
        adsubnumber
    ):
        self.adsubnumber = adsubnumber

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class AdsubSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AdSubscription
        sqla_session = db.session

    idadsub = fields.Integer(dump_only=True)
    adsubnumber = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    subscriber_id = fields.Integer()
    ad_id = fields.Integer()
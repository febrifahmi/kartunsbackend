import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class PesertaWebinar(db.Model):
    __tablename__ = "pesertawebinars"
    idpeserta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namapeserta = db.Column(db.String(80))
    hasilpelatihan = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    training_id = db.Column(db.Integer, db.ForeignKey("trainingwebinars.idwebinar"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    def __init__(
        self,
        namapeserta,
    ):
        self.namapeserta = namapeserta

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class PesertaWebinarSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PesertaWebinar
        sqla_session = db.session

    idpeserta = fields.Integer(dump_only=True)
    namapeserta = fields.String(required=True)
    hasilpelatihan = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    training_id = fields.Integer()
    user_id = fields.Integer()

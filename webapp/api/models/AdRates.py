# ad rates hanya bisa diatur oleh  pengurus / admin

import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields

class AdRates(db.Model):
    __tablename__ = "adrates"
    idadrate = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adratetitle = db.Column(db.String(50))
    adrateperhariharian = db.Column(db.Integer)
    adrateperharibulanan = db.Column(db.Integer)
    adrateperharitahunan = db.Column(db.Integer)
    is_active = db.Column(db.Boolean(), default=0)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    manager_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    def __init__(
        self, adratetitle, adrateperhariharian, adrateperharibulanan, adrateperharitahunan
    ):
        self.adratetitle = adratetitle
        self.adrateperhariharian = adrateperhariharian
        self.adrateperharibulanan = adrateperharibulanan
        self.adrateperharitahunan = adrateperharitahunan

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class AdRatesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AdRates
        sqla_session = db.session

    idadrate = fields.Integer(dump_only=True)
    adratetitle = fields.String(required=True)
    adrateperhariharian = fields.Integer()
    adrateperharibulanan = fields.Integer()
    adrateperharitahunan = fields.Integer()
    is_active = fields.Boolean()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    manager_id = fields.Integer()
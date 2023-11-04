import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class JobOffer(db.Model):
    __tablename__ = "joboffers"
    idoffer = db.Column(db.Integer, primary_key=True, autoincrement=True)
    offertitle = db.Column(db.String(50))
    companylogo = db.Column(db.String(128))
    offerdesc = db.Column(db.String(140))
    offertype = db.Column(db.String(20))
    salaryrange = db.Column(db.String(50))
    offertext = db.Column(db.String(800))
    is_approved = db.Column(db.Boolean)
    is_blocked = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    author_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    def __init__(
        self, offertitle, offerdesc, offertype, salaryrange, offertext, companylogo, file
    ):
        self.offertitle = offertitle
        self.offerdesc = offerdesc
        self.offertype = offertype
        self.salaryrange = salaryrange
        self.offertext = offertext
        self.companylogo = companylogo
        self.file = file

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class JobOfferSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = JobOffer
        sqla_session = db.session

    idoffer = fields.Integer(dump_only=True)
    offertitle = fields.String(required=True)
    companylogo = fields.String()
    offerdesc = fields.String(required=True)
    offertype = fields.String(required=True)
    salaryrange = fields.String(required=True)
    offertext = fields.String(required=True)
    is_approved = fields.Boolean()
    is_blocked = fields.Boolean()
    file = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    author_id = fields.Integer()
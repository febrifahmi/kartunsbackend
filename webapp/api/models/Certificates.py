import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Certificate(db.Model):
    __tablename__ = "certificates"
    idcert = db.Column(db.Integer, primary_key=True, autoincrement=True)
    certtitle = db.Column(db.String(50))
    certbgimgurl = db.Column(db.String(128))
    certnumber = db.Column(db.String(50))
    certtext = db.Column(db.String(800))
    certdate = db.Column(db.Integer, default=7)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    penerima_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    # relationship

    def __init__(
        self, certtitle, certbgimgurl, certnumber, certtext, certdate
    ):
        self.certtitle = certtitle
        self.certbgimgurl = certbgimgurl
        self.certnumber = certnumber
        self.certtext = certtext
        self.certdate = certdate

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class CertificateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Certificate
        sqla_session = db.session

    idcert = fields.Integer(dump_only=True)
    certtitle = fields.String(required=True)
    certbgimgurl = fields.String(required=True)
    certnumber = fields.String(required=True)
    certtext = fields.String(required=True)
    certdate = fields.Integer(required=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    penerima_id = fields.Integer()
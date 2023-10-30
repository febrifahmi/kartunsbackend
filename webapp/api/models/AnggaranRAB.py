import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields

class AnggaranRAB(db.Model):
    __tablename__ = "rab"
    idrab = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rabtitle = db.Column(db.String(50))
    rabdesc = db.Column(db.String(140))
    rabyear = db.Column(db.String(10))
    fileraburi = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk

    # relationship

    def __init__(
        self, rabtitle, rabdesc, rabyear, fileraburi, file
    ):
        self.rabtitle = rabtitle
        self.rabdesc = rabdesc
        self.rabyear = rabyear
        self.fileraburi = fileraburi
        self.file = file

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class AnggaranRABSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AnggaranRAB
        sqla_session = db.session

    idrab = fields.Integer(dump_only=True)
    rabtitle = fields.String(required=True)
    rabdesc = fields.String(required=True)
    rabyear = fields.String()
    fileraburi = fields.String()
    file = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Agenda(db.Model):
    __tablename__ = "agendas"
    idagenda = db.Column(db.Integer, primary_key=True, autoincrement=True)
    judul = db.Column(db.String(80))
    agendaimgurl = db.Column(db.String(128))
    agendadesc = db.Column(db.String(140))
    agendatext = db.Column(db.String(500))
    tanggalmulai = db.Column(db.String(10))
    tanggalselesai = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk

    # relationship

    def __init__(
        self,
        judul,
        agendaimgurl,
        agendadesc,
        agendatext,
        tanggalmulai,
        tanggalselesai,
        file,
    ):
        self.judul = judul
        self.agendaimgurl = agendaimgurl
        self.agendadesc = agendadesc
        self.agendatext = agendatext
        self.tanggalmulai = tanggalmulai
        self.tanggalselesai = tanggalselesai
        self.file = file

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class AgendaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Agenda
        sqla_session = db.session

    idagenda = fields.Integer(dump_only=True)
    judul = fields.String(required=True)
    agendaimgurl = fields.String(required=True)
    agendadesc = fields.String()
    agendatext = fields.String(required=True)
    tanggalmulai = fields.String()
    tanggalselesai = fields.String()
    file = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)

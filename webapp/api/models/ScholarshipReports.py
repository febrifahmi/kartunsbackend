import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class ScholarshipReport(db.Model):
    __tablename__ = "scholarshipreports"
    idreport = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reporttitle = db.Column(db.String(100))
    filereporturi = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    author_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    # relationship

    def __init__(self, reporttitle, filereporturi, file):
        self.reporttitle = reporttitle
        self.filereporturi = filereporturi
        self.file = file

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class ScholarshipReportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ScholarshipReport
        sqla_session = db.session

    idreport = fields.Integer(dump_only=True)
    reporttitle = fields.String(required=True)
    filereporturi = fields.String()
    file = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    author_id = fields.Integer()

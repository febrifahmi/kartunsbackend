import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class PengajuanBeasiswa(db.Model):
    __tablename__ = "pengajuanbeasiswas"
    idpengajuan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namamahasiswa = db.Column(db.String(50))
    batchbeasiswa = db.Column(db.String(10))
    dokproposalbsw = db.Column(db.String(128))
    dokcv = db.Column(db.String(128))
    dokportofolio = db.Column(db.String(128))
    hasilseleksiakhir = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    user_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    # relationship

    def __init__(
        self,
        namamahasiswa,
        batchbeasiswa,
        dokproposalbsw,
        dokcv,
        dokportofolio,
        fileproposalbsw,
        filecv,
        fileportofolio,
        user_id,
    ):
        self.namamahasiswa = namamahasiswa
        self.batchbeasiswa = batchbeasiswa
        self.dokproposalbsw = dokproposalbsw
        self.dokcv = dokcv
        self.dokportofolio = dokportofolio
        self.fileproposalbsw = fileproposalbsw
        self.filecv = filecv
        self.fileportofolio = fileportofolio
        self.user_id = user_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class PengajuanBeasiswaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PengajuanBeasiswa
        sqla_session = db.session

    idpengajuan = fields.Integer(dump_only=True)
    namamahasiswa = fields.String(required=True)
    batchbeasiswa = fields.String(required=True)
    dokproposalbsw = fields.String(required=True)
    dokcv = fields.String(required=True)
    dokportofolio = fields.String(required=True)
    fileproposalbsw = fields.String()
    filecv = fields.String()
    fileportofolio = fields.String()
    hasilseleksiakhir = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    user_id = fields.Integer(required=True)

# barang/jasa
# ads merupakan User generated content (tidak harus dibuat oleh pengurus, tp admin hrs bisa jg buat ads, misal ads campaign utk keperluan organisasi)
# ads harus melalui proses moderasi oleh pengurus
# ads default starting time is now / waktu saat iklan dibuat/publish
# hrs ada field nr of days ads served
# hrs ada field is_blocked (iklan bisa langsung tampil sesuai tanggal tampil jika sudah bayar via VA - midtrans API, moderasi dilakukan dengan is_blocked)

import datetime
from hashlib import md5
from webapp.api.utils.database import db
from webapp.api.utils.database import ma
from marshmallow import fields


class Ad(db.Model):
    __tablename__ = "ads"
    idad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    adcampaigntitle = db.Column(db.String(50))
    adimgurl = db.Column(db.String(128))
    adcampaigndesc = db.Column(db.String(140))
    adcampaigntext = db.Column(db.String(800))
    nrdaysserved = db.Column(db.Integer, default=7)
    kodetagihan = db.Column(db.String())
    totalprice = db.Column(db.Integer())
    is_paid = db.Column(db.Boolean(), default=0)
    is_blocked = db.Column(db.Boolean(), default=1)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # fk
    advertiser_id = db.Column(db.Integer, db.ForeignKey("users.iduser"))

    def __init__(
        self, adcampaigntitle, adimgurl, adcampaigndesc, adcampaigntext, nrdaysserved, kodetagihan, totalprice, file
    ):
        self.adcampaigntitle = adcampaigntitle
        self.adimgurl = adimgurl
        self.adcampaigndesc = adcampaigndesc
        self.adcampaigntext = adcampaigntext
        self.nrdaysserved = nrdaysserved
        self.kodetagihan = kodetagihan
        self.totalprice = totalprice
        self.file = file

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class AdSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ad
        sqla_session = db.session

    idad = fields.Integer(dump_only=True)
    adcampaigntitle = fields.String(required=True)
    adimgurl = fields.String(required=True)
    adcampaigndesc = fields.String()
    adcampaigntext = fields.String(required=True)
    nrdaysserved = fields.Integer()
    kodetagihan = fields.String(required=True)
    totalprice = fields.Integer(required=True)
    is_paid = fields.Boolean()
    is_blocked = fields.Boolean()
    file = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    advertiser_id = fields.Integer()

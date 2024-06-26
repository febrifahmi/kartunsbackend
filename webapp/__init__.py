import os, logging
from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from webapp.api.config.config import ProductionConfig, DevelopmentConfig, TestingConfig
from webapp.api.utils.database import db
from webapp.api.utils.responses import response_with
import webapp.api.utils.responses as resp
from flask_jwt_extended import JWTManager
from webapp.api.utils.seed import (
    seed,
)  # nice it works seeding this way and put BCrypt outside init but without app config
from flask_qrcode import QRcode
from sqlalchemy import create_engine


app = Flask(__name__)

if os.environ.get("ENV") == "PROD":
    appconfig = ProductionConfig
elif os.environ.get("ENV") == "TEST":
    appconfig = TestingConfig
else:
    appconfig = DevelopmentConfig

app.config.from_object(appconfig)
# bcrypt = Bcrypt(app) // we use Bcrypt directly in User model to avoid circular import while seeding initial data to DB
jwt = JWTManager(app)
qrcode = QRcode(app)

# IMPORT ROUTES BLUEPRINT (diimpor setelah seluruh konfigurasi app selesai agar tidak circular import)
from webapp.api.routes.users import user_routes
from webapp.api.routes.ads import ad_routes
from webapp.api.routes.adrates import adrates_routes
from webapp.api.routes.adstransactions import adtransaction_routes
from webapp.api.routes.pengurus import pengurus_routes
from webapp.api.routes.agendas import agenda_routes
from webapp.api.routes.announcements import pengumuman_routes
from webapp.api.routes.articles import article_routes
from webapp.api.routes.certificates import certificate_routes
from webapp.api.routes.comments import comment_routes
from webapp.api.routes.covers import cover_routes
from webapp.api.routes.feedbacks import feedback_routes
from webapp.api.routes.letters import letter_routes
from webapp.api.routes.reactions import reaction_routes
from webapp.api.routes.trainingmaterials import trainmat_routes
from webapp.api.routes.trainings import training_routes
from webapp.api.routes.trainingsubs import tsub_routes
from webapp.api.routes.members import member_routes
from webapp.api.routes.joboffers import joboffer_routes
from webapp.api.routes.suratmasuks import suratmasuk_routes
from webapp.api.routes.feeds import feed_routes
from webapp.api.routes.anggaranrabs import anggaranrab_routes
from webapp.api.routes.anggaranaruskas import anggarankas_routes
from webapp.api.routes.trainingwebinars import trainingwebinar_routes
from webapp.api.routes.donations import donations_routes
from webapp.api.routes.membersiuran import iuranmember_routes
from webapp.api.routes.pesertawebinars import pesertawebinar_routes
from webapp.api.routes.pelamarkerjas import pelamarkerja_routes
from webapp.api.routes.pengajuanbeasiswa import pengajuanbeasiswa_routes
from webapp.api.routes.logtail import logtail_routes


# REG BLUEPRINT
app.register_blueprint(user_routes, url_prefix="/api/users")
app.register_blueprint(ad_routes, url_prefix="/api/ads")
app.register_blueprint(adrates_routes, url_prefix="/api/adrates")
app.register_blueprint(adtransaction_routes, url_prefix="/api/adtransaction")
app.register_blueprint(pengurus_routes, url_prefix="/api/pengurus")
app.register_blueprint(agenda_routes, url_prefix="/api/agendas")
app.register_blueprint(pengumuman_routes, url_prefix="/api/announcements")
app.register_blueprint(article_routes, url_prefix="/api/articles")
app.register_blueprint(certificate_routes, url_prefix="/api/certificates")
app.register_blueprint(comment_routes, url_prefix="/api/comments")
app.register_blueprint(cover_routes, url_prefix="/api/covers")
app.register_blueprint(feedback_routes, url_prefix="/api/feedbacks")
app.register_blueprint(letter_routes, url_prefix="/api/letters")
app.register_blueprint(reaction_routes, url_prefix="/api/reactions")
app.register_blueprint(trainmat_routes, url_prefix="/api/trainingmaterials")
app.register_blueprint(training_routes, url_prefix="/api/trainings")
app.register_blueprint(tsub_routes, url_prefix="/api/tsubs")
app.register_blueprint(member_routes, url_prefix="/api/members")
app.register_blueprint(joboffer_routes, url_prefix="/api/joboffers")
app.register_blueprint(suratmasuk_routes, url_prefix="/api/suratmasuks")
app.register_blueprint(feed_routes, url_prefix="/api/feeds")
app.register_blueprint(anggaranrab_routes, url_prefix="/api/anggaranrabs")
app.register_blueprint(anggarankas_routes, url_prefix="/api/anggarankas")
app.register_blueprint(trainingwebinar_routes, url_prefix="/api/webinars")
app.register_blueprint(donations_routes, url_prefix="/api/donations")
app.register_blueprint(iuranmember_routes, url_prefix="/api/iuranmembers")
app.register_blueprint(pesertawebinar_routes, url_prefix="/api/pesertawebinars")
app.register_blueprint(pelamarkerja_routes, url_prefix="/api/pelamarkerjas")
app.register_blueprint(pengajuanbeasiswa_routes, url_prefix="/api/pengajuanbeasiswa")
app.register_blueprint(logtail_routes, url_prefix="/api/logtail")


# GLOBAL HTTP CONFIGS
@app.after_request
def add_header(response):
    return response


@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)


@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)


@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


db.init_app(app)
with app.app_context():
    """to do: If using mysql, create db if not exist."""
    db.create_all()
    # seed() # nice it works, seeding this way (already fixed in seed.py: double adding admin when there is existing admin in table)
    app.cli.add_command(
        seed
    )  # instead of seeding directly up which causes error in pipenv click when running uwsgi, we register custom flask cli

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)

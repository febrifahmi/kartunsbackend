import os, logging
from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from webapp.api.config.config import ProductionConfig, DevelopmentConfig, TestingConfig
from webapp.api.utils.database import db
from webapp.api.utils.responses import response_with
import webapp.api.utils.responses as resp
from flask_jwt_extended import JWTManager


app = Flask(__name__)

if os.environ.get("WORK_ENV") == "PROD":
    appconfig = ProductionConfig
elif os.environ.get("WORK_ENV") == "TEST":
    appconfig = TestingConfig
else:
    appconfig = DevelopmentConfig

app.config.from_object(appconfig)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# IMPORT ROUTES BLUEPRINT (diimpor setelah seluruh konfigurasi app selesai agar tidak circular import)
from webapp.api.routes.users import user_routes
from webapp.api.routes.ads import ad_routes
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


# REG BLUEPRINT
app.register_blueprint(user_routes, url_prefix="/api/users")
app.register_blueprint(ad_routes, url_prefix="/api/ads")
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
    db.create_all()

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)


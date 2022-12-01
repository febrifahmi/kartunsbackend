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
# from webapp.api.routes.pakets import paket_routes


# REG BLUEPRINT
app.register_blueprint(user_routes, url_prefix="/api/users")
# app.register_blueprint(paket_routes, url_prefix="/api/pakets")



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


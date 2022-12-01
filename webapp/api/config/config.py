import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "JWT-SECRET"
    SECRET_KEY = "SECRET-KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "../../../production.db")
    SECRET_KEY = "SECRET-KEY"
    SECURITY_PASSWORD_SALT = "PASSWORD-SALT"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEVDATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "../../../development.db")
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SECURITY_PASSWORD_SALT = "PASSWORD-SALT"
    MAIL_DEFAULT_SENDER = ""
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    UPLOAD_FOLDER = "images"

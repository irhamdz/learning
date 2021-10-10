# Build the Sqlite ULR for SqlAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_url = "sqlite:///" + os.path.join(basedir, "event.db")
sqlite_url_testing = "sqlite:///" + os.path.join(basedir, "event_test.db")


class Config(object):
    DEBUG = False
    TESTING = False

    # SQLAlchemy
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = sqlite_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://myuser:mypassword@localhost:5672/myvhost')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp://myuser:mypassword@localhost:5672/myvhost')

    # Mailtrap
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'cafdc2968428b1')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '50eaeb2da19dbd')

    # others
    API_DIR = '/api'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = sqlite_url_testing

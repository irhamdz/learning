import pytest

from flask_send_mail import create_app
from flask_send_mail.models import db


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('flask_send_mail.config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
        return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

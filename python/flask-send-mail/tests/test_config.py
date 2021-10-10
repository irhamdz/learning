import os

basedir = os.path.abspath(os.path.dirname(__file__))


def test_development_config(app):
    app.config.from_object('flask_send_mail.config.DevelopmentConfig')
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert "event.db" in app.config['SQLALCHEMY_DATABASE_URI']


def test_testing_config(app):
    app.config.from_object('flask_send_mail.config.TestingConfig')
    assert app.config['DEBUG']
    assert app.config['TESTING']
    assert not app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert "event_test.db" in app.config['SQLALCHEMY_DATABASE_URI']


def test_production_config(app):
    app.config.from_object('flask_send_mail.config.ProductionConfig')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']

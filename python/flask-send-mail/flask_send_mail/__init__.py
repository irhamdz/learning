from flask import render_template, Flask
from flask_restful import Api


def create_app():
    from flask_send_mail.models import db, ma
    from flask_send_mail.event_email import (EventEmailListResource, EventEmailCreateResource, EventEmailResource)
    from flask_send_mail.init_database import init_db_command
    from flask_send_mail.recipient import (RecipientListResource, RecipientResource)

    app = Flask(__name__, template_folder="templates")
    app.config.from_object('flask_send_mail.config.DevelopmentConfig')

    # Initialize Flask-SQLAlchemy
    db.init_app(app)

    # Initialize Flask-Marshmallow
    ma.init_app(app)

    # Initialize Flask-restful resource
    api = Api(app)

    api.add_resource(EventEmailListResource, f'{app.config["API_DIR"]}/event_emails')
    api.add_resource(EventEmailCreateResource, f'{app.config["API_DIR"]}/save_emails')
    api.add_resource(EventEmailResource, f'{app.config["API_DIR"]}/event_emails/<int:id>')
    api.add_resource(RecipientListResource, f'{app.config["API_DIR"]}/recipients')
    api.add_resource(RecipientResource, f'{app.config["API_DIR"]}/recipients/<int:id>')

    @app.route('/')
    def home():
        """
        home page of this app, respond for localhost:5000/
        :return: the rendered template 'home.html'
        """

        return render_template('home.html')

    @app.route('/recipient')
    def recipient():
        """
        This function just responds to the browser URL
        localhost:5000/recipient
        :return: the rendered template "recipient.html"
        """
        return render_template("recipient.html")

    @app.route('/event-email')
    def event_email():
        """
        This function just responds to the browser URL
        localhost:5000/event-email
        :return: the rendered template "event-email.html"
        """
        return render_template("event-email.html")

    # add command
    app.cli.add_command(init_db_command)

    return app

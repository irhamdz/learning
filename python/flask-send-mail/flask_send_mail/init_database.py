import os
from datetime import datetime

import click
from flask.cli import with_appcontext

from flask_send_mail.models import db, Recipient, EventEmail


def init_db():
    EVENT_EMAIL_DATA = [
        {
            "event_id": 1,
            "email_subject": "Future AI Event",
            "email_content": "Lorem ipsum dolor sir amet praesent sapien massa, convallis a pellentesque nec",
            "timestamp": datetime(2021, 4, 10, 23, 00, 00)
        },
        {
            "event_id": 2,
            "email_subject": "Jakarta Fair Event",
            "email_content": "Lorem ipsum dolor sir amet praesent sapien massa, convallis a pellentesque nec",
            "timestamp": datetime(2021, 4, 11, 10, 5, 44)
        },
    ]

    # delete db file if it already exist
    if os.path.exists('event.db'):
        os.remove('event.db')

    # create db
    db.create_all()

    # Populate db
    recipient = Recipient(name="Irham Dzuhri", email="irhamdz@gmail.com")
    db.session.add(recipient)
    for item in EVENT_EMAIL_DATA:
        event_email = EventEmail(
            event_id=item.get('event_id'),
            email_subject=item.get('email_subject'),
            email_content=item.get('email_content'),
            timestamp=item.get('timestamp')
        )
        event_email.recipients.append(recipient)
        db.session.add(event_email)

    db.session.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

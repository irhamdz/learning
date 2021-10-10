import logging
from datetime import datetime

from celery import Celery
from celery.schedules import crontab
from flask_mail import Mail, Message

from flask_send_mail import create_app
from flask_send_mail.helper import construct_timestamp
from flask_send_mail.models import EventEmail, EventEmailSchema

logger = logging.getLogger(__name__)

app = create_app()
app.app_context().push()
mail = Mail(app)
celery = Celery(__name__)

celery.conf.update(
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_url=app.config["CELERY_BROKER_URL"],
    timezone="UTC",
)


@celery.on_after_finalize.connect
def setup_subscription_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/1'),
        send_email.s()
    )


@celery.task(name='send_email')
def send_email():
    with app.app_context():
        event_email = EventEmail.query.all()
        event_email_schema = EventEmailSchema(many=True)
        event_email_data = event_email_schema.dump(event_email)
        for data_event in event_email_data:
            data_timestamp = datetime.strptime(data_event.get('timestamp'), "%Y-%m-%dT%H:%M:%S")
            date_now = datetime.now().replace(microsecond=0)
            # date_now = construct_timestamp('2021-04-10 23:00:00')
            if data_timestamp == date_now:
                # send event email
                with mail.connect() as conn:
                    for recipient in data_event.get('recipients'):
                        logger.info(f"trying sending to {recipient.get('email')}")
                        sender = 'irhamdevs@gmail.com'
                        message = data_event.get('email_content')
                        subject = data_event.get('email_subject')
                        msg = Message(sender=sender,
                                      recipients=[recipient.get('email')],
                                      body=message,
                                      subject=subject)

                        conn.send(msg)
                return 'Message Sent!'

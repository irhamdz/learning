from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# Create the SqlAlchemy db instance
db = SQLAlchemy()

# Initialize Marshmallow
ma = Marshmallow()

event_email_recipient = db.Table('event_email_recipients',
                                 db.Column('recipient_id', db.Integer, db.ForeignKey('recipient.id'), primary_key=True),
                                 db.Column('event_email_id', db.Integer, db.ForeignKey('event_email.id'),
                                           primary_key=True)
                                 )


class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(150), nullable=False)


class RecipientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipient


class EventEmail(db.Model):
    __tablename__ = 'event_email'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    email_subject = db.Column(db.String(150), nullable=False)
    email_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    recipients = db.relationship('Recipient', secondary=event_email_recipient, lazy='subquery',
                                 backref=db.backref('event_emails', lazy=True))


class EventEmailSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EventEmail

    id = ma.auto_field()
    event_id = ma.auto_field()
    email_subject = ma.auto_field()
    email_content = ma.auto_field()
    timestamp = ma.auto_field()
    is_active = ma.auto_field()
    recipients = ma.Nested(RecipientSchema, many=True)

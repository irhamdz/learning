import json

from flask_send_mail import helper
from flask_send_mail.models import Recipient, db, EventEmail

event_email_url = '/api/event_emails'
event_email_save_url = '/api/save_emails'


def create_new_event_emails():
    new_event_email = EventEmail(
        event_id=20,
        email_subject='example subject',
        email_content='example content',
        timestamp=helper.construct_timestamp('2021-04-10 23:00:00')
    )

    db.session.add(new_event_email)
    db.session.commit()

    return new_event_email


def test_get_event_emails(client):
    response = client.get(event_email_url)
    assert response.status_code == 200


def test_get_all_event_emails(client):
    response = client.get(f'{event_email_url}?included_deleted=true')
    assert response.status_code == 200


def test_not_found_event_emails(client):
    response = client.get(f'{event_email_url}/10')
    assert response.status_code == 404


def test_add_event_emails(client):
    post_data = {
        "event_id": 40,
        "email_subject": "Test New Subject",
        "email_content": "Test New Content Email",
        "timestamp": '2021-04-10 23:10:10'
    }
    response = client.post(event_email_save_url,
                           data=json.dumps(post_data),
                           content_type='application/json'
                           )
    data_event_email = EventEmail.query.filter_by(event_id=post_data.get('event_id')).one_or_none()
    assert response.status_code == 201
    assert data_event_email is not None


def test_add_recipients_to_event_emails(client):
    new_event_email_data = create_new_event_emails()

    patch_data = {
        "recipients": [1, 2]
    }
    response = client.patch(f'{event_email_url}/{new_event_email_data.id}',
                            data=json.dumps(patch_data),
                            content_type='application/json'
                            )
    data_event_email = EventEmail.query.filter_by(id=new_event_email_data.id).one_or_none()
    assert response.status_code == 200


def test_patch_event_emails(client):
    new_event_email_data = create_new_event_emails()

    patch_data = {
        "email_content": "This is new content"
    }
    response = client.patch(f'{event_email_url}/{new_event_email_data.id}',
                            data=json.dumps(patch_data),
                            content_type='application/json'
                            )
    data_event_email = EventEmail.query.filter_by(id=new_event_email_data.id).one_or_none()
    assert response.status_code == 200
    assert data_event_email.email_content == patch_data.get('email_content')


def test_delete_recipients(client):
    new_event_email_data = create_new_event_emails()

    new_event_email_data = EventEmail.query.filter_by(id=new_event_email_data.id).one_or_none()
    response = client.delete(f'{event_email_url}/{new_event_email_data.id}')
    data_recipient = EventEmail.query.filter_by(id=new_event_email_data.id).one_or_none()
    assert response.status_code == 204
    assert not data_recipient.is_active

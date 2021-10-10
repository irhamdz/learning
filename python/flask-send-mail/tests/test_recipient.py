import json

from flask_send_mail.models import Recipient, db

recipient_url = '/api/recipients'


def create_new_recipient():
    new_recipient = Recipient(
        name='john',
        email='john@test.com',
    )

    db.session.add(new_recipient)
    db.session.commit()

    return Recipient.query.filter_by(email=new_recipient.email).one_or_none()


def test_get_recipients(client):
    response = client.get(recipient_url)
    assert response.status_code == 200


def test_add_recipients(client):
    post_data = {
        "name": "irham",
        "email": "irhamtest@gmail.com"
    }
    response = client.post(recipient_url,
                           data=json.dumps(post_data),
                           content_type='application/json'
                           )
    data_recipient = Recipient.query.filter_by(email=post_data.get('email')).one_or_none()
    assert response.status_code == 201
    assert data_recipient is not None


def test_patch_recipients(client):
    new_recipient_data = create_new_recipient()

    patch_data = {
        "email": "irhamtest@gmail.com"
    }
    response = client.patch(f'{recipient_url}/{new_recipient_data.id}',
                            data=json.dumps(patch_data),
                            content_type='application/json'
                            )
    data_recipient = Recipient.query.filter_by(email=patch_data.get('email')).one_or_none()
    assert response.status_code == 200
    assert data_recipient.email == patch_data.get('email')


def test_delete_recipients(client):
    new_recipient = create_new_recipient()

    new_recipient_data = Recipient.query.filter_by(email=new_recipient.email).one_or_none()
    response = client.delete(f'{recipient_url}/{new_recipient_data.id}')
    data_recipient = Recipient.query.filter_by(email='john@test.com').one_or_none()
    assert response.status_code == 204
    assert data_recipient is None

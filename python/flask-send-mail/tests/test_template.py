def test_index_page(client):
    response = client.get('/')
    assert b"Home Page" in response.data
    assert b"Event Email Application" in response.data


def test_event_email_page(client):
    response = client.get('/event-email')
    assert b"Event Email Page" in response.data
    assert b"Event Email Create/Update/Delete" in response.data
    assert b"Event Email Lists" in response.data


def test_recipient_page(client):
    response = client.get('/recipient')
    assert b"Recipient Page" in response.data
    assert b"Recipient Create/Update/Delete" in response.data
    assert b"Recipient Lists" in response.data

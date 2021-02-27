import pytest


def test_not_staff_access(client, auth):
    # guest access
    assert client.get('/admin/').status_code == 403

    # not staff user access
    auth.login(username='other', password='other')
    assert client.get('/admin/').status_code == 403


def test_staff_access(client, auth):
    auth.login()
    assert client.get('/admin/').status_code == 200

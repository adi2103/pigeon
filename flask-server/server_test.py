import pytest
import mock
import os
from server import create_app, TESTING_CALL_SID
from http.client import HTTPException


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(
            os.environ,
            {
                "TWILIO_ACCOUNT_SID": "ACebd6cd2cf151d10cc31d86e6ea3a8219",
                "TWILIO_AUTH_TOKEN": "250d6c28e5b498beb713b6e988290335",
            }):
        yield


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_call_happy_path(client):
    response = client.post("/calls", json={
        "phone_number": "+447881412467",
        "message": "Hi there!",
    })
    assert response.json["call_sid"] == TESTING_CALL_SID


def test_call_failure(client):
    with pytest.raises(HTTPException):
        client.post("/calls", json={
            "phone_number": "+44788sdfsd2467",
            "message": "Hi there!",
        })

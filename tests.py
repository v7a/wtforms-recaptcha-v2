import json
from http.server import BaseHTTPRequestHandler, HTTPStatus
from socketserver import TCPServer
from threading import Thread
from urllib.parse import parse_qs

import pytest

from wtforms import ValidationError

from wtforms_recaptcha_v2 import RecaptchaV2Validator, RecaptchaV2FormMixin


class Field:
    def __init__(self, data):
        self.data = data


class RecaptchaRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle captcha responses."""
        data = parse_qs(self.rfile.read(int(self.headers["content-length"])).decode("utf-8"))
        resp = json.dumps({"success": data["response"][0] == "True"})
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp.encode("utf-8"))


@pytest.fixture
def recaptcha_service():
    with TCPServer(("", 0), RecaptchaRequestHandler) as httpd:
        thread = Thread(target=httpd.serve_forever)
        thread.start()
        yield httpd
        httpd.shutdown()
        thread.join()


def make_url(service):
    return "http://localhost:{}".format(service.server_address[1])


def make_validator(url, raise_on_connection_error=False):
    return RecaptchaV2Validator(
        "secret key", raise_on_connection_error=raise_on_connection_error, verification_url=url,
    )


def test_validator_bad(recaptcha_service):
    with pytest.raises(ValidationError):
        make_validator(make_url(recaptcha_service))(None, Field(False))


def test_validator_good(recaptcha_service):
    make_validator(make_url(recaptcha_service))(None, Field(True))


def test_validator_no_connection():
    # o.k., don't harm user experience
    make_validator("http://invalidservice:11111")(None, Field(True))


def test_validator_no_connection_fail():
    with pytest.raises(ValidationError):
        make_validator("http://invalidservice:11111", raise_on_connection_error=True)(
            None, Field(True)
        )

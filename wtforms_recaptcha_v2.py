"""Provides a wtforms validator to validate a recaptcha v2 response and a form mixin to create a form
field for recaptcha v2 with the possibility to disable validation altogether under certain
circumstances.
"""

from typing import Protocol, Optional

import requests
from requests import HTTPError, Timeout, ConnectionError as ConnError

from wtforms import ValidationError, StringField

__version__ = "0.1"


class MakeErrorMessage(Protocol):
    """Make an error message."""

    def __call__(self, form: type) -> str:
        pass


class GetRemoteIP(Protocol):
    """Get the remote IP of the current request."""

    def __call__(self, form: type) -> Optional[str]:
        pass


class RecaptchaV2Validator:
    """Validate a recaptcha response.

    By default, if the service is unavailable, validation passes to not degrade user experience.

    The verification service optionally takes a remoteip field to check if the one solving the
    captcha actually submitted the form. A callback taking the form instance as parameter allows
    you to provide the remote IP regardless of which toolkit or framework you use.

    The reason why error messages are retrieved via a callback is to give you the possibility to
    translate the messages without being dependent on this library to provide all of them for you.
    Each callback takes the associated form instance as parameter from which you can use any state
    you like. Defaults are provided for English.

    :param secret_key: Secret key generated by the captcha administration service
    :param get_remote_ip: Get remote IP of the current request
    :param make_error_msg: Make error message if captcha verification fails
    :param make_connection_error_msg: Make error message if service is unavailable
    :param raise_on_connection_error: Pass or fail validation if service is unavailable
    """

    def __init__(
        self,
        secret_key: Optional[str],
        request_timeout: float = 2000.0,
        get_remote_ip: GetRemoteIP = lambda _: None,
        make_error_msg: MakeErrorMessage = lambda _: "Captcha verification failed.",
        make_connection_error_msg: MakeErrorMessage = lambda _: "Verification service unavailable.",
        raise_on_connection_error: bool = False,
        verification_url: str = "https://www.google.com/recaptcha/api/siteverify",
    ):
        self.secret_key = secret_key
        self.request_timeout = request_timeout
        self.make_error_msg = make_error_msg
        self.make_connection_error_msg = make_connection_error_msg
        self.get_remote_ip = get_remote_ip
        self.raise_on_connection_error = raise_on_connection_error
        self.verification_url = verification_url

    def _collect_data(self, form, field) -> dict:
        data = {}
        data["secret"] = self.secret_key
        data["response"] = field.data

        remoteip = self.get_remote_ip(form)
        if remoteip is not None:
            data["remoteip"] = remoteip

        return data

    def __call__(self, form, field):
        try:
            if not requests.post(
                self.verification_url, self._collect_data(form, field), timeout=self.request_timeout
            ).json()["success"]:
                raise ValidationError(self.make_error_msg(form))
        except (HTTPError, Timeout, ConnError):
            if self.raise_on_connection_error:
                raise ValidationError(self.make_connection_error_msg(form))


try:
    import wtforms_field_factory

    class RecaptchaV2FormMixin:
        """A form mixin that defines the recaptcha V2 field only if the secret key in the validator
        instance is a truthy value."""

        def __init__(self, validator: RecaptchaV2Validator):
            self.validator = validator

        @wtforms_field_factory.field(
            name="g-recaptcha-response", enable_if=lambda self: self.validator.secret_key
        )
        def _captcha_v2_field(self):
            return StringField(label="recaptcha", validators=[self.validator])


except ImportError:
    pass  # o.k., cannot use mixin

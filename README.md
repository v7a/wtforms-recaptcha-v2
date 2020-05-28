# wtforms Google Recaptcha v2
Provides a wtforms validator to validate a recaptcha v2 response and a form mixin to create a form
field for recaptcha v2 with the possibility to disable validation altogether under certain
circumstances.

The form mixin requires [wtforms-field-factory](https://github.com/v7a/wtforms-field-factory). Not
having this dependency installed simply does not define the form mixin class.

## Contributing
Before committing, run the following and check if it succeeds:
```sh
pip install --user -r requirements-dev.txt && \
black wtforms_field_factory.py && \
pylint wtforms_field_factory.py && \
pytest && \
coverage report --fail-under=100
```

import pytest

from app.cli import createsuperuser, create_db


def test_createsuperuser(app):
    runner = app.test_cli_runner()

    result = runner.invoke(createsuperuser, ['--username', 'cli_admin', '--password', '--pass'])
    assert 'Super user create successfully.' in result.output

    result = runner.invoke(createsuperuser, input='input_admin\npass')
    assert 'Super user create successfully.' in result.output


def test_create_db(app):
    runner = app.test_cli_runner()

    result = runner.invoke(create_db)
    assert 'Database create successfully.' in result.output


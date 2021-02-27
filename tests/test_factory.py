import pytest
from app import create_app

from tests.conftest import TestConfig


def test_config():
    assert not create_app().testing
    assert create_app(TestConfig).testing

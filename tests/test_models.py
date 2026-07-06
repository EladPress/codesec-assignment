"""Validation tests for the request schema."""
import pytest
from pydantic import ValidationError

from app.models import MeasureRequest


def test_valid_request():
    req = MeasureRequest(url="https://example.com", frequency=5)
    assert str(req.url) == "https://example.com/"
    assert req.frequency == 5
    assert req.duration == 600  # default = 10 minutes


def test_negative_frequency_rejected():
    with pytest.raises(ValidationError):
        MeasureRequest(url="https://example.com", frequency=-1)


def test_zero_frequency_rejected():
    with pytest.raises(ValidationError):
        MeasureRequest(url="https://example.com", frequency=0)


def test_malformed_url_rejected():
    with pytest.raises(ValidationError):
        MeasureRequest(url="not-a-url", frequency=5)

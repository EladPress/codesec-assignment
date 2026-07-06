"""Unit tests for the measurement core."""
import httpx
import respx

from app.measure import measure_once


@respx.mock
async def test_measure_success():
    respx.get("https://example.com").mock(
        return_value=httpx.Response(200, text="ok")
    )
    sample = await measure_once("https://example.com")

    assert sample["url"] == "https://example.com"
    assert sample["status_code"] == 200
    assert sample["success"] is True
    assert sample["error"] is None
    assert sample["latency_ms"] >= 0
    assert "timestamp" in sample


@respx.mock
async def test_measure_non_2xx_is_not_success():
    respx.get("https://example.com").mock(return_value=httpx.Response(503))
    sample = await measure_once("https://example.com")

    assert sample["status_code"] == 503
    assert sample["success"] is False
    assert sample["error"] is None  # a 503 is a valid response, not an error


@respx.mock
async def test_measure_network_error_is_recorded_not_raised():
    respx.get("https://example.com").mock(
        side_effect=httpx.ConnectError("boom")
    )
    sample = await measure_once("https://example.com")

    assert sample["success"] is False
    assert sample["status_code"] is None
    assert "ConnectError" in sample["error"]


@respx.mock
async def test_measure_timeout_is_recorded():
    respx.get("https://example.com").mock(
        side_effect=httpx.TimeoutException("timed out")
    )
    sample = await measure_once("https://example.com")

    assert sample["success"] is False
    assert "Timeout" in sample["error"]

"""Measurement core: one timed HTTP request → one sample.

This module is intentionally free of any web or scheduling concerns so it can be
unit-tested in isolation and reused (e.g. from a CLI) later.
"""
import time
from datetime import datetime, timezone

import httpx

from .config import FOLLOW_REDIRECTS, REQUEST_TIMEOUT


async def measure_once(url: str, timeout: float = REQUEST_TIMEOUT) -> dict:
    """Perform a single GET against ``url`` and return a structured sample.

    Never raises on network errors: a failure is recorded in the sample with
    ``success=False`` so the surrounding measurement loop keeps running.
    """
    start = time.perf_counter()
    sample: dict = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "url": url,
    }
    try:
        async with httpx.AsyncClient(
            timeout=timeout, follow_redirects=FOLLOW_REDIRECTS
        ) as client:
            resp = await client.get(url)
        sample.update(
            latency_ms=round((time.perf_counter() - start) * 1000, 2),
            status_code=resp.status_code,
            success=resp.is_success,
            error=None,
        )
    except httpx.HTTPError as exc:
        # Timeout, DNS failure, connection refused, invalid response, etc.
        sample.update(
            latency_ms=round((time.perf_counter() - start) * 1000, 2),
            status_code=None,
            success=False,
            error=f"{type(exc).__name__}: {exc}",
        )
    return sample

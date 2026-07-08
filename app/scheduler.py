"""Measurement scheduler: repeat a single measurement on a fixed cadence.

Per the chosen design, each tick is exactly one HTTP request to the target
(not a batch). Requests are fired every ``frequency`` seconds for ``duration``
seconds total.
"""
import asyncio
import sys
import time

from .emit import emit
from .measure import measure_once


def _hms(seconds: float) -> str:
    """Format a non-negative duration in seconds as ``HH:MM:SS``."""
    total = int(max(0.0, seconds))
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


async def run_job(url: str, frequency: float, duration: float) -> None:
    """Measure ``url`` once every ``frequency`` seconds for ``duration`` seconds."""
    start = time.monotonic()
    deadline = start + duration
    print(
        f"[scheduler] starting job url={url} frequency={frequency}s "
        f"duration={duration}s",
        file=sys.stderr,
        flush=True,
    )

    while time.monotonic() < deadline:
        tick_start = time.monotonic()
        sample = await measure_once(url)
        sample["elapsed"] = _hms(tick_start - start)
        sample["remaining"] = _hms(deadline - tick_start)
        emit(sample)
        # Subtract the request's own duration so samples land on a steady
        # wall-clock cadence rather than drifting as latency grows.
        tick_duration = time.monotonic() - tick_start
        await asyncio.sleep(max(0.0, frequency - tick_duration))

    print(f"[scheduler] job complete url={url}", file=sys.stderr, flush=True)

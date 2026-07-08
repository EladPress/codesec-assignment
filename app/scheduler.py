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
        sample["elapsed_seconds"] = round(tick_start - start, 2)
        sample["remaining_s"] = round(max(0.0, deadline - tick_start), 2)
        emit(sample)
        # Subtract the request's own duration so samples land on a steady
        # wall-clock cadence rather than drifting as latency grows.
        tick_duration = time.monotonic() - tick_start
        await asyncio.sleep(max(0.0, frequency - tick_duration))

    print(f"[scheduler] job complete url={url}", file=sys.stderr, flush=True)

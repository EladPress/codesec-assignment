"""Sample output.

Isolated behind a single function so the destination (stdout today, a database
or metrics backend tomorrow) can change without touching the measurement loop.
"""
import json
import sys


def emit(sample: dict) -> None:
    """Write one sample to stdout as a single JSON line.

    ``flush=True`` ensures samples appear in real time when redirected to a
    file (e.g. ``> samples.txt``) instead of being buffered.
    """
    print(json.dumps(sample), file=sys.stdout, flush=True)

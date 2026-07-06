"""Service configuration and defaults.

Values are read from environment variables so the service is easy to deploy
across environments (12-factor style) without code changes.
"""
import os

# Per-request timeout when measuring the target resource (seconds).
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "10.0"))

# Default duration of a measurement job if the payload omits it (seconds).
# 600s = 10 minutes, matching assignment requirement 1c.
DEFAULT_DURATION = float(os.getenv("DEFAULT_DURATION", "600"))

# Follow redirects when measuring (a 30x + redirect chain is real latency).
FOLLOW_REDIRECTS = os.getenv("FOLLOW_REDIRECTS", "true").lower() == "true"

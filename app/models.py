"""Pydantic request/response schemas — the service's public contract.

Validation lives here so malformed input is rejected at the edge with a clear
HTTP 422 before any measurement logic runs.
"""
from pydantic import BaseModel, Field, HttpUrl

from .config import DEFAULT_DURATION


class MeasureRequest(BaseModel):
    """Payload for POST /measure."""

    url: HttpUrl = Field(
        ...,
        description="Public HTTP(S) resource whose latency should be measured.",
    )
    frequency: float = Field(
        ...,
        gt=0,
        le=3600,
        description="Seconds between measurements. One request is made per interval.",
    )
    duration: float = Field(
        default=DEFAULT_DURATION,
        gt=0,
        description="Total seconds to run the job (default 600 = 10 minutes).",
    )


class MeasureResponse(BaseModel):
    """Acknowledgement returned when a measurement job is accepted."""

    job_id: str
    url: str
    frequency: float
    duration: float
    status: str

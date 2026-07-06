"""FastAPI application — the web layer.

Accepts a measurement request, validates it, and launches a background job that
streams samples to stdout. Returns 202 Accepted immediately.
"""
import uuid

from fastapi import BackgroundTasks, FastAPI

from .models import MeasureRequest, MeasureResponse
from .scheduler import run_job

app = FastAPI(title="Latency Measurement Service", version="0.1.0")


@app.get("/health")
async def health() -> dict:
    """Liveness/readiness probe target for Kubernetes."""
    return {"status": "ok"}


@app.post("/measure", response_model=MeasureResponse, status_code=202)
async def measure(req: MeasureRequest, background_tasks: BackgroundTasks) -> MeasureResponse:
    """Start a background job that measures ``req.url`` on a fixed cadence."""
    job_id = str(uuid.uuid4())
    background_tasks.add_task(
        run_job, str(req.url), req.frequency, req.duration
    )
    return MeasureResponse(
        job_id=job_id,
        url=str(req.url),
        frequency=req.frequency,
        duration=req.duration,
        status="started",
    )

"""
main.py
────────
LeadPilot AI — FastAPI application entry point.

Responsibilities:
  - Create the FastAPI app with metadata for auto-generated docs.
  - Configure structured logging.
  - Register all routers.
  - Add CORS middleware (open for demo; restrict origins in production).
  - Expose a root redirect to /docs for convenience.

Run with:
    uvicorn app.main:app --reload --port 8000
"""

import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.config import settings
from app.routes.lead import router as lead_router


# ── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO if settings.APP_ENV != "development" else logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=(
        "**LeadPilot AI** powers AI-driven lead intake and response automation. "
        "Submit a lead → receive a personalised AI email + scheduling link."
    ),
    contact={
        "name":  "LeadPilot AI",
        "email": settings.EMAIL_FROM_ADDRESS,
    },
    docs_url="/docs",
    redoc_url="/redoc",
)


# ── CORS ─────────────────────────────────────────────────────────────────────
# For the live demo, allow all origins.
# In production, replace ["*"] with your frontend domain(s).
ALLOWED_ORIGINS = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(lead_router, tags=["Leads"])


# ── Root redirect ─────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    """Redirect root to the interactive API docs."""
    return RedirectResponse(url="/docs")


# ── Startup / shutdown events ─────────────────────────────────────────────────
@app.on_event("startup")
async def on_startup() -> None:
    logger.info(
        "🚀 %s v%s starting in [%s] mode",
        settings.APP_TITLE,
        settings.APP_VERSION,
        settings.APP_ENV,
    )


@app.on_event("shutdown")
async def on_shutdown() -> None:
    logger.info("LeadPilot AI shutting down.")

"""
routes/lead.py
───────────────
FastAPI router defining the two public endpoints:

  POST /lead    — Receive a lead, run the AI pipeline, send the email.
  GET  /health  — Liveness check used by load balancers / monitoring.

The in-memory lead store (lead_store) is a module-level dict keyed by lead
UUID.  For a production deployment swap this for a database (Postgres, etc.)
or a cache (Redis) without touching any other part of the codebase.
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.models.lead import LeadRequest, LeadRecord, LeadResponse
from app.services.ai_service       import generate_lead_response
from app.services.email_service    import send_lead_response_email
from app.services.calendar_service import generate_scheduling_link
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# ── In-memory lead store ────────────────────────────────────────────────────
# dict[lead_id: str → LeadRecord]
# Persists for the lifetime of the process — perfectly fine for a live demo.
lead_store: dict[str, LeadRecord] = {}


# ── POST /lead ───────────────────────────────────────────────────────────────

@router.post(
    "/lead",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new lead",
    description=(
        "Accepts lead data from the frontend form, generates a personalised "
        "AI response email, sends it to the lead, and returns a confirmation "
        "with a scheduling link."
    ),
)
async def submit_lead(payload: LeadRequest) -> LeadResponse:
    """
    Full lead-intake pipeline:
      1. Validate incoming data (handled by Pydantic).
      2. Generate a Google Calendar scheduling link.
      3. Call OpenAI to write the personalised email.
      4. Send the email via SMTP.
      5. Persist the enriched record in memory.
      6. Return a structured confirmation to the frontend.
    """
    lead_id = str(uuid.uuid4())
    logger.info(
        "New lead received | id=%s name=%r company=%r email=%r",
        lead_id, payload.name, payload.company, payload.email,
    )

    # ── Step 1: Generate scheduling link ────────────────────────────────────
    scheduling_link = generate_scheduling_link(
        name=payload.name,
        email=payload.email,
        company=payload.company,
    )

    # ── Step 2: AI email generation ─────────────────────────────────────────
    try:
        ai_email_body = await generate_lead_response(
            name=payload.name,
            company=payload.company,
            message=payload.message,
            scheduling_link=scheduling_link,
        )
    except RuntimeError as exc:
        logger.error("AI generation failed for lead %s: %s", lead_id, exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI service unavailable: {exc}",
        )

    # ── Step 3: Send email (non-fatal — we still store the lead) ────────────
    email_sent  = False
    email_error = None

    try:
        await send_lead_response_email(
            to_name=payload.name,
            to_email=payload.email,
            ai_email_body=ai_email_body,
            company=payload.company,
        )
        email_sent = True
    except RuntimeError as exc:
        # Email failure is logged and recorded but does NOT 500 the request.
        # The AI response is still stored so it can be retried later.
        email_error = str(exc)
        logger.warning(
            "Email send failed for lead %s (%s): %s",
            lead_id, payload.email, exc,
        )

    # ── Step 4: Persist record ───────────────────────────────────────────────
    record = LeadRecord(
        id=lead_id,
        received_at=datetime.now(timezone.utc),
        name=payload.name,
        email=payload.email,
        company=payload.company,
        message=payload.message,
        ai_response=ai_email_body,
        scheduling_link=scheduling_link,
        email_sent=email_sent,
        email_error=email_error,
    )
    lead_store[lead_id] = record

    logger.info(
        "Lead %s stored | email_sent=%s",
        lead_id, email_sent,
    )

    # ── Step 5: Return response ──────────────────────────────────────────────
    return LeadResponse(
        status="success" if email_sent else "partial",
        lead_id=lead_id,
        message=(
            "Lead received and response email sent successfully."
            if email_sent
            else "Lead received. AI response generated but email delivery failed — check logs."
        ),
        scheduling_link=scheduling_link,
        ai_response_preview=ai_email_body[:200],
    )


# ── GET /health ──────────────────────────────────────────────────────────────

@router.get(
    "/health",
    summary="Health check",
    description="Returns API status and a count of leads stored in memory.",
)
async def health_check() -> dict[str, Any]:
    """
    Liveness / readiness endpoint.
    Returns 200 as long as the process is running.
    """
    return {
        "status": "ok",
        "app": settings.APP_TITLE,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "leads_in_memory": len(lead_store),
    }

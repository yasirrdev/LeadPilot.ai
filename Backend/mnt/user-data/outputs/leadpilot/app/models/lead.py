"""
models/lead.py
──────────────
Pydantic models that define the shape of lead data flowing through the system.
FastAPI uses these for automatic request validation and OpenAPI docs.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class LeadRequest(BaseModel):
    """Payload received from the frontend contact form."""
    name: str       = Field(..., min_length=1, max_length=120, examples=["Jane Smith"])
    email: EmailStr = Field(..., examples=["jane@acme.com"])
    company: str    = Field(..., min_length=1, max_length=120, examples=["Acme Corp"])
    message: str    = Field(..., min_length=5, max_length=2000,
                            examples=["We're looking for a CRM solution for our sales team."])


class LeadRecord(LeadRequest):
    """Enriched record stored in memory after the AI pipeline completes."""
    id: str                        # unique UUID
    received_at: datetime
    ai_response: str               # the generated email body
    scheduling_link: str           # calendar URL sent to lead
    email_sent: bool = False       # True once SMTP delivery succeeds
    email_error: str | None = None # populated if delivery failed


class LeadResponse(BaseModel):
    """JSON returned to the frontend after a successful /lead call."""
    status: str
    lead_id: str
    message: str
    scheduling_link: str
    ai_response_preview: str  # first 200 chars — useful for UI confirmation

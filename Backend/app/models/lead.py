"""
models/lead.py
───────────────
Pydantic models for the lead intake pipeline.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class LeadRequest(BaseModel):
    """Incoming payload from the frontend form."""
    name: str
    email: EmailStr
    company: str
    message: str


class LeadRecord(LeadRequest):
    """Full persisted record — extends LeadRequest with server-side fields."""
    id: str
    received_at: datetime
    ai_response: Optional[str] = None
    scheduling_link: Optional[str] = None
    email_sent: bool = False
    email_error: Optional[str] = None


class LeadResponse(BaseModel):
    """Response returned to the frontend after lead submission."""
    status: str          # "success" | "partial"
    lead_id: str
    message: str
    scheduling_link: Optional[str] = None
    ai_response_preview: Optional[str] = None  # first 200 chars

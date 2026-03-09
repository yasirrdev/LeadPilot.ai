"""
services/calendar_service.py
─────────────────────────────
Generates a scheduling / booking link for the lead.

For the demo, this produces a Google Calendar Appointment Scheduling URL
pre-filled with the lead's name and email so they land on a ready-to-book
page with no friction.

To upgrade to a real integration:
  - Replace CALENDAR_BASE_URL with your actual Google Calendar schedule ID.
  - Or swap the URL builder for a Calendly / Cal.com API call.
  - Google Calendar Appointment Scheduling docs:
    https://support.google.com/calendar/answer/10729749
"""

import logging
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

from app.config import settings

logger = logging.getLogger(__name__)


def generate_scheduling_link(name: str, email: str, company: str) -> str:
    """
    Build a personalised scheduling link for the lead.

    Google Calendar Appointment pages accept query parameters that pre-fill
    the booking form, reducing friction for the lead.

    Args:
        name:    Lead's full name.
        email:   Lead's email address.
        company: Lead's company name (appended to the name field).

    Returns:
        A full URL string the lead can click to book a call.
    """
    base_url = settings.CALENDAR_BASE_URL

    # Query parameters supported by Google Calendar appointment pages
    params = {
        "name":  f"{name} ({company})",
        "email": email,
    }

    # Safely append query params regardless of whether base_url already has some
    parsed = urlparse(base_url)
    existing_params = parse_qs(parsed.query)
    existing_params.update({k: [v] for k, v in params.items()})

    # Flatten list values back to single strings for urlencode
    flat_params = {k: v[0] for k, v in existing_params.items()}
    new_query = urlencode(flat_params)

    scheduling_url = urlunparse(parsed._replace(query=new_query))

    logger.info("Scheduling link generated for %s <%s>", name, email)
    return scheduling_url

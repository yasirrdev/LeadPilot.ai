"""
services/email_service.py
──────────────────────────
Sends the AI-generated response email to the lead over SMTP (TLS/STARTTLS).

Uses aiosmtplib so sending never blocks the FastAPI event loop.
Supports Gmail, SendGrid SMTP relay, Mailgun, and any standard SMTP provider.
"""

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.config import settings

logger = logging.getLogger(__name__)


def _build_mime_message(
    to_name: str,
    to_email: str,
    subject: str,
    plain_body: str,
) -> MIMEMultipart:
    """
    Construct a MIME email with both plain-text and a minimal HTML version.
    Having both parts improves deliverability and rendering across clients.
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM_ADDRESS}>"
    msg["To"]      = f"{to_name} <{to_email}>"

    # Plain-text part (shown by clients that block HTML)
    msg.attach(MIMEText(plain_body, "plain", "utf-8"))

    # Minimal HTML part — wraps plain text in readable formatting
    html_body = (
        "<html><body style='font-family:Arial,sans-serif;line-height:1.6;"
        "color:#333;max-width:600px;margin:auto;padding:24px;'>"
        + plain_body.replace("\n\n", "</p><p>").replace("\n", "<br>")
        + "<hr style='border:none;border-top:1px solid #eee;margin-top:32px;'>"
        "<p style='font-size:12px;color:#999;'>Sent by LeadPilot AI</p>"
        "</body></html>"
    )
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    return msg


async def send_lead_response_email(
    to_name: str,
    to_email: str,
    ai_email_body: str,
    company: str,
) -> None:
    """
    Send the AI-generated email to the lead.

    Args:
        to_name:       Lead's full name (used in MIME To header).
        to_email:      Lead's email address.
        ai_email_body: Plain-text email body from the AI service.
        company:       Lead's company — used to personalise the subject line.

    Raises:
        RuntimeError: wraps any SMTP / network error with a descriptive message.
    """
    subject = f"Re: Your enquiry from {company} — Let's connect!"

    msg = _build_mime_message(
        to_name=to_name,
        to_email=to_email,
        subject=subject,
        plain_body=ai_email_body,
    )

    logger.info("Sending email to %s <%s>", to_name, to_email)

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            start_tls=True,   # STARTTLS on port 587 (switch to use_tls=True for port 465)
        )
        logger.info("Email delivered successfully to %s", to_email)

    except aiosmtplib.SMTPException as exc:
        logger.error("SMTP error sending to %s: %s", to_email, exc, exc_info=True)
        raise RuntimeError(f"Email delivery failed (SMTP): {exc}") from exc

    except Exception as exc:
        logger.error("Unexpected error sending email to %s: %s", to_email, exc, exc_info=True)
        raise RuntimeError(f"Email delivery failed: {exc}") from exc

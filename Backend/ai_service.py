"""
services/ai_service.py
──────────────────────
Calls the OpenAI Chat Completions API to generate a personalised response
email for an incoming lead.

The prompt instructs the model to act as a professional sales assistant —
it thanks the lead, acknowledges their message, asks 1-2 qualifying
questions, and invites them to book a call via the scheduling link.
"""

import logging
from openai import AsyncOpenAI
from app.config import settings

logger = logging.getLogger(__name__)

# Initialise the async client once at module load; reused across requests
_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


SYSTEM_PROMPT = """
You are Alex, a friendly and professional sales assistant at LeadPilot AI.
Your job is to respond to incoming business inquiries with warmth, clarity,
and a consultative tone.

When writing a response email you MUST:
1. Start with a genuine thank-you for reaching out.
2. Briefly acknowledge the specific topic or problem they mentioned.
3. Ask exactly 1–2 focused qualifying questions that help understand
   their needs, budget, or timeline — never more.
4. Invite them to book a discovery call using the scheduling link provided.
5. Close with a professional, upbeat sign-off.

Rules:
- Write in plain text only — no markdown, no bullet points in the email body.
- Keep the email under 200 words.
- Do NOT fabricate product details or pricing.
- Always refer to the company as "LeadPilot AI".
- Address the lead by their first name only.
""".strip()


def _build_user_prompt(
    name: str,
    company: str,
    message: str,
    scheduling_link: str,
) -> str:
    """Compose the user-turn message sent to the model."""
    return (
        f"Lead details:\n"
        f"  Name: {name}\n"
        f"  Company: {company}\n"
        f"  Message: {message}\n\n"
        f"Scheduling link to include in your reply: {scheduling_link}\n\n"
        "Write the full response email now."
    )


async def generate_lead_response(
    name: str,
    company: str,
    message: str,
    scheduling_link: str,
) -> str:
    """
    Generate a personalised response email for a lead.

    Returns:
        The email body as a plain-text string.

    Raises:
        RuntimeError: if the OpenAI call fails, with context for logging.
    """
    logger.info("Generating AI email for lead: %s <%s>", name, company)

    try:
        response = await _client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": _build_user_prompt(name, company, message, scheduling_link),
                },
            ],
            temperature=0.7,   # slight creativity while staying professional
            max_tokens=400,    # keeps the email concise
        )

        email_body: str = response.choices[0].message.content.strip()
        logger.info("AI email generated successfully (%d chars)", len(email_body))
        return email_body

    except Exception as exc:
        logger.error("OpenAI call failed: %s", exc, exc_info=True)
        raise RuntimeError(f"AI generation failed: {exc}") from exc

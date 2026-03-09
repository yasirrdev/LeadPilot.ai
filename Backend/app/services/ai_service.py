"""
services/ai_service.py
──────────────────────
Generates a personalised response email for an incoming lead using a
local Ollama instance (http://localhost:11434, model: mistral).

Public API — unchanged from the OpenAI version so routes/lead.py needs
no modification:

    await generate_lead_response(name, company, message, scheduling_link)
    generate_ai_response(prompt)   ← low-level helper, also exported

Fallback behaviour:
  If Ollama is unreachable or returns an error the function logs the
  problem and returns a safe, pre-written template email instead of
  raising — the lead is never lost.
"""

import logging
import textwrap

import requests

logger = logging.getLogger(__name__)

# ── Ollama config ─────────────────────────────────────────────────────────────
OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"
TIMEOUT_SEC  = 60   # generous — first run pulls weights from disk

# ── Prompt template ───────────────────────────────────────────────────────────
_PROMPT_TEMPLATE = textwrap.dedent("""
    You are Alex, a friendly and professional sales assistant at LeadPilot AI.
    Write a short response email (under 200 words, plain text only, no markdown)
    to the following lead:

    Name:    {name}
    Company: {company}
    Message: {message}

    Your email MUST:
    1. Open with a genuine thank-you and address the lead by first name.
    2. Briefly acknowledge the specific topic they mentioned.
    3. Ask exactly 1-2 focused qualifying questions about their needs or timeline.
    4. Invite them to book a discovery call using this link: {scheduling_link}
    5. Close with a professional, upbeat sign-off from Alex at LeadPilot AI.

    Write the email now:
""").strip()

# ── Fallback template ─────────────────────────────────────────────────────────
_FALLBACK_TEMPLATE = textwrap.dedent("""
    Hi {first_name},

    Thank you for reaching out to LeadPilot AI! We received your inquiry
    from {company} and we're excited to learn more about how we can help.

    Could you share a bit more about your current challenges and your
    ideal timeline for getting started?

    In the meantime, feel free to book a quick discovery call here:
    {scheduling_link}

    Looking forward to connecting!

    Best,
    Alex
    LeadPilot AI
""").strip()


# ── Core function ─────────────────────────────────────────────────────────────

def generate_ai_response(prompt: str) -> str:
    """
    Send *prompt* to the local Ollama instance and return the response text.

    Args:
        prompt: The fully-formed prompt string to send to the model.

    Returns:
        Generated text from Ollama, or an empty string on failure
        (callers should handle the empty-string case).

    Raises:
        Never — all exceptions are caught and logged.
    """
    payload = {
        "model":  OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=TIMEOUT_SEC,
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("response", "").strip()
        logger.debug("Ollama returned %d chars", len(text))
        return text

    except requests.exceptions.ConnectionError:
        logger.warning(
            "Ollama is not running at %s — using fallback response.", OLLAMA_URL
        )
    except requests.exceptions.Timeout:
        logger.warning(
            "Ollama timed out after %ds — using fallback response.", TIMEOUT_SEC
        )
    except requests.exceptions.HTTPError as exc:
        logger.warning("Ollama HTTP error %s — using fallback response.", exc)
    except Exception as exc:
        logger.error("Unexpected Ollama error: %s", exc, exc_info=True)

    return ""  # signals fallback to the caller


# ── Public high-level function (same signature as the old OpenAI version) ─────

async def generate_lead_response(
    name: str,
    company: str,
    message: str,
    scheduling_link: str,
) -> str:
    """
    Generate a personalised response email for a lead.

    Tries Ollama first; falls back to a pre-written template if unavailable.
    Never raises — the caller (routes/lead.py) can always proceed.

    Returns:
        Email body as a plain-text string.
    """
    logger.info("Generating AI email for lead: %s @ %s", name, company)

    prompt = _PROMPT_TEMPLATE.format(
        name=name,
        company=company,
        message=message,
        scheduling_link=scheduling_link,
    )

    email_body = generate_ai_response(prompt)

    if email_body:
        logger.info("Ollama email generated successfully (%d chars)", len(email_body))
        return email_body

    # ── Fallback ──────────────────────────────────────────────────────────────
    logger.warning("Falling back to predefined email template for lead: %s", name)
    first_name = name.split()[0] if name else name
    return _FALLBACK_TEMPLATE.format(
        first_name=first_name,
        company=company,
        scheduling_link=scheduling_link,
    )

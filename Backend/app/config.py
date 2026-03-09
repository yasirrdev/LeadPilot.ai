"""
config.py
─────────
Centralised settings loaded from environment variables via python-dotenv.
All services import from here — never read os.environ directly elsewhere.
"""

import os
from dotenv import load_dotenv

# Load .env file if present (no-op in prod where vars are injected by the host)
load_dotenv()


class Settings:
    # ── App ──────────────────────────────────────────────────────────────
    APP_TITLE: str       = os.getenv("APP_TITLE", "LeadPilot AI")
    APP_VERSION: str     = os.getenv("APP_VERSION", "1.0.0")
    APP_ENV: str         = os.getenv("APP_ENV", "development")
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    # ── OpenAI ───────────────────────────────────────────────────────────
    OPENAI_API_KEY: str  = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str    = os.getenv("OPENAI_MODEL", "gpt-4o")

    # ── SMTP ─────────────────────────────────────────────────────────────
    SMTP_HOST: str       = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int       = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str   = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str   = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM_NAME: str    = os.getenv("EMAIL_FROM_NAME", "LeadPilot AI")
    EMAIL_FROM_ADDRESS: str = os.getenv("EMAIL_FROM_ADDRESS", "")

    # ── Google Calendar ───────────────────────────────────────────────────
    CALENDAR_BASE_URL: str = os.getenv(
        "CALENDAR_BASE_URL",
        "https://calendar.google.com/calendar/appointments/schedules/DEMO"
    )


# Singleton — import `settings` everywhere
settings = Settings()

# LeadPilot AI — Backend

> AI-powered lead intake and response automation built with FastAPI + OpenAI.

---

## What it does

1. Receives a lead from a frontend contact form (`POST /lead`).
2. Calls **OpenAI GPT-4o** to generate a personalised sales response email.
3. Sends the email automatically to the lead via **SMTP**.
4. Returns a **Google Calendar scheduling link** so the lead can book a call.
5. Stores the enriched lead record in memory for the session.

---

## Project structure

```
leadpilot/
├── app/
│   ├── main.py                  # FastAPI app, CORS, router registration
│   ├── config.py                # Settings loaded from .env
│   ├── models/
│   │   └── lead.py              # Pydantic models (LeadRequest, LeadRecord, LeadResponse)
│   ├── routes/
│   │   └── lead.py              # POST /lead  |  GET /health
│   └── services/
│       ├── ai_service.py        # OpenAI call — generates the email
│       ├── email_service.py     # aiosmtplib — sends the email
│       └── calendar_service.py  # Builds the Google Calendar scheduling URL
├── .env.example                 # Copy → .env and fill in your credentials
├── requirements.txt
└── README.md
```

---

## Prerequisites

| Tool    | Version  |
|---------|----------|
| Python  | 3.11+    |
| pip     | latest   |

---

## Quickstart

### 1. Clone / download and enter the project directory

```bash
cd leadpilot
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in:

| Variable              | Description                                      |
|-----------------------|--------------------------------------------------|
| `OPENAI_API_KEY`      | Your OpenAI API key (sk-...)                     |
| `SMTP_HOST`           | SMTP server hostname (e.g. `smtp.gmail.com`)     |
| `SMTP_PORT`           | SMTP port — `587` for STARTTLS, `465` for SSL    |
| `SMTP_USERNAME`       | Your sending email address                       |
| `SMTP_PASSWORD`       | App password (Gmail) or SMTP password            |
| `EMAIL_FROM_ADDRESS`  | Displayed as the sender                          |
| `CALENDAR_BASE_URL`   | Your Google Calendar Appointment schedule URL    |

**Gmail tip:** use an [App Password](https://support.google.com/accounts/answer/185833), not your account password.

### 5. Run the server

```bash
uvicorn app.main:app --reload --port 8000
```

The API is now live at **http://localhost:8000**  
Interactive docs: **http://localhost:8000/docs**

---

## Endpoints

### `POST /lead`

Accepts lead data, runs the full AI pipeline, and sends the email.

**Request body (JSON):**

```json
{
  "name":    "Jane Smith",
  "email":   "jane@acme.com",
  "company": "Acme Corp",
  "message": "We're evaluating CRM tools for our 20-person sales team."
}
```

**Response (201 Created):**

```json
{
  "status":                "success",
  "lead_id":               "a1b2c3d4-...",
  "message":               "Lead received and response email sent successfully.",
  "scheduling_link":       "https://calendar.google.com/...",
  "ai_response_preview":   "Hi Jane, thank you so much for reaching out!..."
}
```

---

### `GET /health`

```json
{
  "status":           "ok",
  "app":              "LeadPilot AI",
  "version":          "1.0.0",
  "environment":      "development",
  "leads_in_memory":  3
}
```

---

## Testing with curl

### Submit a lead

```bash
curl -s -X POST http://localhost:8000/lead \
  -H "Content-Type: application/json" \
  -d '{
    "name":    "Jane Smith",
    "email":   "jane@acme.com",
    "company": "Acme Corp",
    "message": "We are evaluating CRM tools for our 20-person sales team and would love to learn more about your platform."
  }' | python -m json.tool
```

### Health check

```bash
curl -s http://localhost:8000/health | python -m json.tool
```

---

## Notes for production

- Replace the in-memory `lead_store` dict with **PostgreSQL** or **Redis**.
- Set `allow_origins` in CORS to your actual frontend domain.
- Add **rate limiting** (e.g. `slowapi`) to the `/lead` endpoint.
- Store `SMTP_PASSWORD` and `OPENAI_API_KEY` in a secrets manager (AWS Secrets Manager, GCP Secret Manager, etc.).
- Add a background task queue (e.g. **Celery + Redis**) if email volume grows.

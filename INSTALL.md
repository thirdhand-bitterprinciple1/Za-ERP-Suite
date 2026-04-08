# Install Guide

This guide covers local setup and Docker setup for ZA ERP Suite.

## Requirements

- Python 3.11+
- pip
- virtualenv support (`python3 -m venv`)
- Redis (for Celery background tasks)
- Optional: Docker + Docker Compose

## Local Setup (Recommended for Development)

1. Clone and enter project root.
2. Create environment file:

```bash
cp backend/.env.example backend/.env
```

3. Edit `backend/.env` and set a secure `DJANGO_SECRET_KEY`.
4. Create and activate virtual environment:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

7. Seed demo users/data (optional):

```bash
python manage.py seed_demo_access --reset-passwords --rotate-tokens
```

8. Start backend API:

```bash
python manage.py runserver 0.0.0.0:8000
```

## Start Celery Worker

In a separate terminal:

```bash
cd backend
source .venv/bin/activate
celery -A config worker -l info
```

## Docker Setup

1. Ensure `backend/.env` exists.
2. Start stack:

```bash
docker compose up --build
```

## API Docs

- OpenAPI Schema: `/api/schema/`
- Swagger UI: `/api/docs/swagger/`
- ReDoc: `/api/docs/redoc/`

## Troubleshooting

- If auth fails, re-check token and `X-Company-ID` header.
- If reports stay pending, ensure Redis + Celery worker are running.
- If demo passwords mismatch, rotate them:

```bash
python manage.py rotate_demo_access
```

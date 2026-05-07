# Bioval — Backend

Django REST API for the Bioval biomass data management platform. Uses Clerk for authentication, PostgreSQL (Neon) for the database, Stripe for subscriptions, and serves a Next.js frontend.

---

## Tech Stack

- **Python 3.14+**
- **Django 6** + **Django REST Framework**
- **PostgreSQL** (via Neon or local)
- **Clerk** (JWT authentication)
- **Stripe** (subscriptions)
- **Whitenoise** (static files)
- **Gunicorn** (production server)

---

## Prerequisites

Make sure you have the following installed:

- Python 3.11+
- pip
- git
- A PostgreSQL database (local or [Neon](https://neon.tech) free tier)
- A [Clerk](https://clerk.com) account
- A [Stripe](https://stripe.com) account (optional for local dev)

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-org/bioval-backend.git
cd bioval-backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the `.env` file

Create a `.env` file at the root of the project:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/bioval
# Or your Neon connection string:
# DATABASE_URL=postgresql://user:password@ep-xxx.eu-west-1.aws.neon.tech/bioval?sslmode=require

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Frontend
FRONTEND_URL=http://localhost:3000

# Clerk
CLERK_JWKS_URL=https://your-clerk-domain.clerk.accounts.dev/.well-known/jwks.json

# Stripe (can use dummy values for local dev if not testing payments)
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_PRICE_ID=price_xxx
```

> **Where to find these values:**
> - `SECRET_KEY`: generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
> - `DATABASE_URL`: your local PostgreSQL URL or Neon connection string
> - `CLERK_JWKS_URL`: in your Clerk dashboard → API Keys → JWKS URL (looks like `https://xxx.clerk.accounts.dev/.well-known/jwks.json`)
> - `STRIPE_*`: in your Stripe dashboard → Developers → API Keys

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a test user (optional)

Since this project uses Clerk for auth, there's no `createsuperuser`. Instead, insert a user directly via the Django shell:

```bash
python manage.py shell
```

```python
from apps.users.models import User
User.objects.create(
    clerk_id="test_admin",
    email="admin@example.com",
    nom="Admin",
    prenom="Test",
    role="admin_global",
    is_active=True,
)
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`.

---

## Project Structure

```
bioval-backend/
├── apps/
│   ├── users/          # Custom user model, Clerk JWT auth, permissions
│   ├── datasets/       # Dataset & Famille models, upload, validation
│   ├── access_requests/# External user access request flow
│   ├── groups/         # Group management
│   ├── subscriptions/  # Stripe subscription management
│   └── logs/           # Activity logging
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/sync/` | Sync Clerk user to DB (called on login) |
| GET | `/api/users/me/` | Get current user |
| GET/PATCH/DELETE | `/api/users/<id>/` | Manage a user |
| GET/POST | `/api/datasets/` | List datasets / Upload |
| GET/PATCH/DELETE | `/api/datasets/<id>/` | Dataset detail |
| GET/POST | `/api/familles/` | List / Create families |
| GET/POST | `/api/requests/` | List access requests / Submit |
| GET/PATCH | `/api/requests/<id>/` | Review a request |
| GET/POST | `/api/groups/` | List / Create groups |
| POST | `/api/groups/<id>/members/` | Add member |
| DELETE | `/api/groups/<id>/members/<user_id>/` | Remove member |
| GET | `/api/subscriptions/` | List subscriptions |
| POST | `/api/subscriptions/checkout/` | Create Stripe checkout |
| POST | `/api/subscriptions/webhook/` | Stripe webhook |
| GET | `/api/logs/` | Activity logs |

---

## User Roles

| Role | Description |
|------|-------------|
| `admin_global` | Full platform access |
| `admin_metier` | Validates datasets and access requests |
| `admin_externe` | Manages their company's group and subscription |
| `user_interne` | Can upload and view validated datasets |
| `user_externe` | Same as interne, conditioned on subscription |

---

## Running in Production

The project is deployed on **Render** (free tier). See deployment notes:

- Static files are served via Whitenoise
- Database is hosted on Neon (PostgreSQL)
- Gunicorn is used as the WSGI server

Build command:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

Start command:
```bash
gunicorn core.wsgi:application
```

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ | Django secret key |
| `DEBUG` | ✅ | `True` for local, `False` for production |
| `ALLOWED_HOSTS` | ✅ | Comma-separated list of allowed hosts |
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `CORS_ALLOWED_ORIGINS` | ✅ | Frontend URL (no trailing slash) |
| `FRONTEND_URL` | ✅ | Frontend URL for Stripe redirects |
| `CLERK_JWKS_URL` | ✅ | Clerk JWKS endpoint for JWT verification |
| `STRIPE_SECRET_KEY` | ✅ | Stripe secret key |
| `STRIPE_WEBHOOK_SECRET` | ✅ | Stripe webhook signing secret |
| `STRIPE_PRICE_ID` | ✅ | Stripe price ID for subscription plan |
# Django Customer Management Platform

A complete, production-style **Customer Relationship Management (CRM)** REST API built with Django and Django REST Framework. It manages customers (individuals), companies, contacts, addresses, documents, tasks, relationship history and observations, with JWT authentication, role-based permissions, an audit trail and an async task worker.

This project was built as a portfolio piece to demonstrate clean architecture, test-driven development and production-ready tooling (containerization, CI/CD) on a realistic business domain.

## Features

- **Customers & Companies** — full CRUD for individual clients (with CPF validation) and corporate clients (with CNPJ validation).
- **Contacts, Addresses, Documents** — each linked to exactly one Customer *or* one Company, enforced at both the API and database level (`CheckConstraint`).
- **Tasks** — assignable to-dos with due dates, status/priority tracking, and an async email notification sent via Celery when a task is assigned.
- **Relationship history & observations** — a timeline of interactions (calls, emails, meetings) and free-form notes per client.
- **Authentication** — JWT access/refresh tokens (`djangorestframework-simplejwt`), registration, login, current-user profile, password change.
- **Authorization** — Django's built-in Users, Groups and Permissions exposed through the API; staff-only endpoints for user/group management.
- **Audit log** — every create/update/delete performed through the API is recorded (who, what, when, before/after).
- **Admin panel** — Django's built-in admin, which supports both light and dark themes out of the box (Django 5).
- **Validation** — CPF/CNPJ check-digit validation, phone/ZIP code format validation, file size limits on uploads, business-rule validation (e.g. a task's due date cannot be in the past).
- **Filtering, search, ordering & pagination** on every list endpoint.

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Framework | Django 5.1 + Django REST Framework |
| Database | PostgreSQL 16 |
| Cache / broker | Redis 7 |
| Async tasks | Celery |
| Auth | JWT (`djangorestframework-simplejwt`) |
| Tests | Pytest + pytest-django + factory_boy |
| Lint / format | Ruff + Black |
| Containers | Podman / Docker + Compose |
| CI/CD | GitHub Actions |

## Architecture

The codebase is organized as small, focused Django apps, each owning one bounded context:

```
customer_management/      # project settings, URLs, Celery app (split settings: base/dev/prod/test)
apps/
  core/                    # shared abstractions: base models, validators, pagination,
                           # audit logging mixin, custom exception handler
  accounts/                # custom User model, JWT auth, Users/Groups/Permissions API
  customers/               # Customer aggregate (individuals)
  companies/               # Company aggregate (organizations)
  crm/                     # Contact, Address, Document, Task, RelationshipHistory,
                           # Observation — all linked to exactly one Customer or Company
```

Domain rules that matter (e.g. "a record belongs to exactly one party", "a task cannot be created with a past due date", CPF/CNPJ validity) live in serializers/validators/model constraints close to the models — not scattered across views — keeping the write path thin and testable.

Every write performed through the API is audited via an `AuditLoggingMixin` that viewsets opt into, recording the acting user, the action and a snapshot of the change in an `AuditLogEntry`.

## Getting started

### Prerequisites

- Python 3.13
- [Podman](https://podman.io/) (or Docker) + Compose

### Run with Podman (recommended)

```bash
cp .env.example .env
podman compose up -d --build
podman exec -it django-customer-management-web-1 python manage.py createsuperuser
```

The API is now available at `http://localhost:8010/api/`, and the admin panel at `http://localhost:8010/admin/`.

> Ports are intentionally mapped to non-default host ports (`15432` for PostgreSQL, `16380` for Redis, `8010` for the app) to avoid clashing with other local services.

To stop everything:

```bash
podman compose down
```

### Run locally without containers

```bash
python -m venv .venv
.venv/Scripts/activate        # .venv/bin/activate on Linux/macOS
pip install -r requirements/dev.txt
cp .env.example .env          # point POSTGRES_* / REDIS_URL at your own services
python manage.py migrate
python manage.py runserver
```

## Running tests

```bash
pytest
```

Tests run against an in-memory SQLite database (see `customer_management/settings/test.py`) with Celery in eager mode, so no external services are required. The suite covers models, validators, and every CRUD endpoint (success and validation-failure paths) with ~98% statement coverage on `apps/`.

## API overview

All endpoints are under `/api/` and require a JWT `Authorization: Bearer <token>` header, except where noted.

| Endpoint | Description |
|---|---|
| `POST /api/auth/register/` | Create a new account (public) |
| `POST /api/auth/login/` | Obtain access/refresh tokens (public) |
| `POST /api/auth/refresh/` | Refresh an access token |
| `GET/PATCH /api/auth/me/` | Current user profile |
| `POST /api/auth/change-password/` | Change the current user's password |
| `/api/auth/users/`, `/api/auth/groups/` | User & group management (staff only for writes) |
| `/api/auth/permissions/` | Read-only list of Django permissions |
| `/api/customers/` | Customer CRUD |
| `/api/companies/` | Company CRUD |
| `/api/contacts/`, `/api/addresses/`, `/api/documents/` | CRUD, linked to a customer or a company |
| `/api/tasks/` | Task CRUD, with async email notification on assignment |
| `/api/relationship-history/` | Interaction log CRUD |
| `/api/observations/` | Free-form notes CRUD |

Every list endpoint supports `?search=`, `?ordering=`, pagination (`?page=`, `?page_size=`) and model-specific filters (e.g. `?status=ACTIVE`, `?customer=<id>`).

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on every push/PR to `master`: Ruff lint, Black format check, the full Pytest suite with coverage, a Django deployment check, and a container image build.

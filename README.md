# ZA ERP Suite

Open-source, modular ERP backend for growing businesses.

## What This Project Is

ZA ERP Suite is a Django + DRF based business platform with:

- Multi-company tenant isolation
- Role-based access control
- Approval workflows
- Audit trail logging
- Event-driven module integration
- Background reporting with Celery + Redis
- Real-time notifications using SSE

## Current Scope

The current repository contains the backend platform.

Implemented modules:

- CRM
- Website
- Commerce
- Inventory
- Purchasing
- Accounting
- Billing
- HR
- Projects
- Reports
- Core (auth, audit, notifications, org context)

## Core Features

### Security and Tenancy

- Token auth endpoint: `POST /api/auth/token/`
- Company context header: `X-Company-ID`
- Company membership and role checks at API layer

### Approval Workflow

Business actions follow:

`Draft -> Pending Approval -> Completed`

- Sales orders require manager/admin approval
- Purchase orders require manager/admin approval

### Audit Trail

- Generic audit log model tracks create/update/delete
- Captures user, timestamp, old values, new values, and target object

### Background Reports

- Monthly P&L report jobs run in Celery
- PDF reports are generated and downloadable

### Notifications

- In-app notifications API
- SSE stream endpoint for real-time updates
- Mark one / mark all as read endpoints
- Deep-link metadata support (`target_path`, `target_id`)

## Documentation

- Installation guide: [INSTALL.md](INSTALL.md)
- Business scenarios: [USECASE.md](USECASE.md)
- Contribution guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- License: [LICENSE](LICENSE)

## Quick Start

For complete setup steps, see [INSTALL.md](INSTALL.md).

Fast path:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## API Docs

- OpenAPI Schema: `/api/schema/`
- Swagger UI: `/api/docs/swagger/`
- ReDoc: `/api/docs/redoc/`

## Useful API Endpoints

- `GET /api/orgs/companies/`
- `GET /api/orgs/memberships/`
- `GET /api/core/audit-logs/`
- `GET /api/core/notifications/`
- `POST /api/core/notifications/{id}/mark_read/`
- `POST /api/core/notifications/mark_all_read/`
- `GET /api/core/notifications/stream/?token=<token>&company_id=<id>`
- `POST /api/reports/jobs/`
- `GET /api/reports/jobs/`
- `GET /api/reports/jobs/{id}/download/`

## Status

- Backend active
- Frontend removed from this repository

## License

AGPL-3.0-only. See [LICENSE](LICENSE).

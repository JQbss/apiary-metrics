# 🐝 Apiary Metrics

A REST API for managing apiaries and analyzing beekeeping data. Built with Django, PostgreSQL and Docker.

## About

Apiary Metrics is a personal project for beekeepers to track their hives, queens, inspections, harvests, expenses and sales in one place.

## Features

- 🏡 **Apiary management** – create and manage multiple apiaries
- 🐝 **Hive tracking** – monitor hive strength, aggression level and type
- 👑 **Queen management** – track queens, their types and notes
- 🔍 **Hive inspections** – log inspection history per hive
- 🍯 **Harvest tracking** – record harvests by type
- 💰 **Expenses & Sales** – track costs and revenue with categories
- 📋 **Notes** – add notes to apiaries and queens
- 📖 **Swagger UI** – interactive API documentation at `/api/docs/`

## Tech Stack

- **Backend:** Django 5.1, Django REST Framework
- **Auth:** JWT (SimpleJWT)
- **Database:** PostgreSQL
- **Containerization:** Docker
- **Docs:** drf-spectacular (OpenAPI / Swagger)
- **Other:** django-environ, django-cors-headers, Whitenoise, Pillow

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:
```bash
git clone https://github.com/JQbss/apiary-metrics.git
cd apiary-metrics
```

2. Create `env/.env.local` and fill in the required variables:
```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=your-secret-key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=apiary_metrics
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DOCS_USERNAME=admin
DOCS_PASSWORD=admin
```

3. Build and run:
```bash
docker compose up --build
```

4. Run migrations:
```bash
docker compose exec web python manage.py migrate
```

5. Create superuser:
```bash
docker compose exec web python manage.py createsuperuser
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/api/docs/`
- Admin panel: `http://localhost:8000/admin/`

Authentication uses Bearer JWT tokens. Obtain a token via `/api/users/token/` and include it in the `Authorization` header.

## Project Structure

```
src/
├── apps/
│   ├── apiaries/
│   ├── hives/
│   ├── queens/
│   ├── harvests/
│   ├── expenses/
│   ├── sales/
│   └── users/
├── core/
│   └── settings/
└── utils/
```

## Status

Active development — personal side project.

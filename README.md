# data_sharing

Django-based platform for request-driven file collection and sharing.

## Overview
This repository contains a web application for collecting and managing shared files with support for OAuth logins, background processing, and billing integrations.

## Features
- Space and request-based data sharing workflows
- Custom Google and Microsoft OAuth providers
- Asynchronous tasks with Celery + Redis
- Stripe integration via `dj-stripe`
- Docker-based deployment configuration
- Product documentation in `docs/`

## Tech Stack
- Python 3
- Django 5
- PostgreSQL
- Celery + Redis
- Stripe / dj-stripe
- TailwindCSS

## Repository Structure
- `data_sharing/`: Django project settings and URL configuration
- `web_app/`: application logic and views
- `custom_google_provider/`, `custom_microsoft_provider/`: OAuth provider integrations
- `templates/`, `static/`: frontend templates and assets
- `docs/`: user-facing product documentation
- `readme/`: additional setup notes

## Quick Start
1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure `config/secret.py` with your local credentials and keys.
4. Start required services (PostgreSQL and Redis).
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the app:
   ```bash
   python manage.py runserver
   ```

## Optional Local Services
- Celery worker:
  ```bash
  celery -A web_app worker -l INFO
  ```
- Celery beat:
  ```bash
  celery -A web_app beat -l INFO
  ```
- Stripe webhooks in local development can be tested with `ngrok`.

## Documentation
- Product docs entrypoint: `docs/home.md`
- Additional setup notes: `readme/setup-app.md`

## Status
Maintained as a personal/project codebase and reference implementation.

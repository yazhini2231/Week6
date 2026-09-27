# Car Rental Application – Python Full Stack

A student-friendly full-stack car rental application built with Flask, SQLite, HTML, CSS and JavaScript.

## Features
- Vehicle listings
- Booking management
- Demo payment status
- Booking confirmation
- Vehicle/booking tracking status
- REST API for vehicles
- Health-check endpoint
- SQLite persistence
- Production start command using Gunicorn

## Run locally

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Test

```bash
pytest -q
```

## Deploy to Render

Build command:
```bash
pip install -r requirements.txt
```

Start command:
```bash
gunicorn app:app
```

Add `SECRET_KEY` as an environment variable in the hosting dashboard. Do not commit secrets.

## Important note
The payment feature is a demonstration only. It does not process real card payments. A production application should integrate a PCI-compliant payment provider and never store raw card details.

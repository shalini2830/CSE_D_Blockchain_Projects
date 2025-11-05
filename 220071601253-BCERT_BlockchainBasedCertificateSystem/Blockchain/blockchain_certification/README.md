# Blockchain Certificate Verification (Django)

A simple, private blockchain-backed certificate issuance and verification system.

## Features
- Issue certificates; each issuance creates a new block with PoW and links to previous hash
- Verify by certificate ID or QR link
- Minimal, clean HTML/CSS frontend (no frameworks)
- PostgreSQL by default, SQLite3 fallback automatically
- Optional: PDF export, revoke/reissue, chain visualization

## Setup

### 1) Requirements
- Python 3.10+
- pip
- (Optional) PostgreSQL server

### 2) Create virtual environment and install deps
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\pip install django psycopg2-binary qrcode pillow reportlab
# macOS/Linux
source .venv/bin/activate
pip install django psycopg2-binary qrcode pillow reportlab
```

### 3) Configure DB (optional)
Set environment variables for PostgreSQL or leave blank to use SQLite:
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- POSTGRES_PORT

### 4) Migrate and run
```bash
# from blockchain_certification/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

### 5) Create default institution (optional)
In Django shell:
```bash
python manage.py shell
```
```python
from users.views import ensure_default_institution
ensure_default_institution()
exit()
```
Login via `admin@example.com` / `admin123` at `/login/`.

## How it works
- When issuing a certificate, we compute SHA-256 over a canonical payload of fields.
- A new block is mined with a simple PoW (`0000` prefix target) and linked to the previous block hash.
- We store block metadata in DB; verification ensures the certificate hash exists in the chain and that links are consistent.

## QR Verification
- Each certificate page embeds a QR image linking to `/verify/<certificate_id>/`.

## Optional Enhancements
- Revoke/reissue flow (set `status` on `Certificate`)
- PDF rendering using `reportlab`
- Visual chain view at `/chain/`

## Project Structure
```
blockchain_certification/
├── blockchain/
├── certificates/
├── users/
├── templates/
├── static/
├── manage.py
└── README.md
```

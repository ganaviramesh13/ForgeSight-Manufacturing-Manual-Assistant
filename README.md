# ForgeSight — Manufacturing Manual Assistant

A Django + Django REST Framework hackathon MVP implementing the supplied Round 1 brief. It ingests the three supplied PDFs with PyMuPDF, stores page-preserving passages in MySQL or SQLite, restricts retrieval to the selected machine, and records questions, answers, statuses, and citations.

## Quick start (Windows PowerShell)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```
Open `http://127.0.0.1:8000/`. Demo users: `admin`, `engineer`, `supervisor`; password `demo1234`.

For MySQL set `DB_ENGINE=mysql` and the DB variables in `.env`, create the database first, then run migrations. SQLite is the zero-setup fallback for the demonstration.

## Load the supplied corpus
Log in as `admin`, choose `/upload/`, and upload only the three PDFs in `Round1StudentPack/Manuals`, using metadata from `machine_manual_index.csv`. The upload screen extracts page-by-page text and chunks it while retaining machine, document, revision, and PDF page metadata.

## Demo checklist
1. As admin, upload all three manuals and show processed corpus.
2. As engineer, select HP-200 and ask “What does E17 mean?”; inspect the HP-OPS-01 page 2 citation.
3. Ask the HP-200 question about E17 and first inspection checks; the answer should cite both current HP-200 manuals.
4. Select AC-90 and ask about the AF-10 check/replacement interval.
5. Ask an AC-90-only question while HP-200 is selected; show insufficient evidence.
6. Attempt `/upload/` as engineer; server returns 403.
7. Sign in as supervisor and review the question history.

## API
- `GET /api/machines/`
- `POST /ask/` with `machine_id`, `question` and CSRF token (authenticated)
- `POST /upload/` multipart PDF upload (admin only)

## Architecture
Browser → Django views/DRF-compatible JSON endpoints → MySQL/SQLite models → PyMuPDF page extraction → machine-filtered lexical retrieval → extractive evidence answer → Question/Citation history. The fallback is deliberately extractive and does not invent unsupported numbers. An external LLM provider can be added behind `OPENAI_API_KEY` without placing keys in source code.

## Tests
```powershell
python manage.py test
```
The included tests cover engineer upload denial and machine-scoped retrieval. Production hardening should add provider contract tests, upload size limits, rate limiting, and a true embedding index if required by the judging environment.

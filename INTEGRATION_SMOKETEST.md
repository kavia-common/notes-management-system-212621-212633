# Notes App Integration & Smoke Test

This document summarizes the final integration checks and a simple smoke test to validate end-to-end functionality across the Database, Backend (FastAPI), and Frontend (React).

## 1) Configuration summary

- Frontend API base URL
  - File: notes_frontend/src/api/client.js
  - Default: http://localhost:3001
  - Override: set env var REACT_APP_API_BASE_URL

- Backend DATABASE_URL
  - File: notes_backend/src/api/config.py
  - Default: postgresql://appuser:dbuser123@localhost:5000/myapp
  - Can be overridden by DATABASE_URL env var.

- Backend CORS
  - File: notes_backend/src/api/main.py (via settings.ALLOWED_ORIGINS)
  - Default allowed origin(s): http://localhost:3000
  - Override: ALLOWED_ORIGINS env var (comma-separated list)

- Backend OpenAPI
  - File (generated): notes_backend/interfaces/openapi.json
  - Generator: notes_backend/src/api/generate_openapi.py

## 2) Start the database (PostgreSQL)

In the notes_database folder:
- Use startup script to ensure Postgres is running on port 5000 and schema/seed are applied.

Commands (example):
1) ./notes_database/startup.sh
2) Verify connection info: notes_database/db_connection.txt
   Example connection string: psql postgresql://appuser:dbuser123@localhost:5000/myapp

Ensure the "notes" table exists (schema.sql creates it). The backend expects integer IDs if you use the provided backend schema; if using the supplied notes_database schema with UUID IDs, adjust backend accordingly (see "Notes" below).

## 3) Start the backend (FastAPI)

In notes_backend:
- Install requirements
- Start server on 0.0.0.0:3001 (default for uvicorn examples)

Example:
  pip install -r notes_backend/requirements.txt
  uvicorn src.api.main:app --host 0.0.0.0 --port 3001

Health check:
  GET http://localhost:3001/

Docs:
  http://localhost:3001/docs

## 4) Start the frontend (React)

In notes_frontend:
- Use default base URL (http://localhost:3001) or set REACT_APP_API_BASE_URL

Example:
  export REACT_APP_API_BASE_URL=http://localhost:3001
  npm install
  npm start

App URL:
  http://localhost:3000

## 5) Smoke test: Create -> Edit -> Delete

Steps:
1) Load http://localhost:3000 (ensure browser console shows no CORS errors)
2) Create:
   - Click "＋ New"
   - Verify new "Untitled note" appears in list and is selected
3) Edit:
   - Enter a title (e.g., "Test Note")
   - Enter some content
   - Click "💾 Save"
   - Verify list shows updated title, and no error alerts
4) Delete:
   - Click trash icon on the created note
   - Confirm deletion
   - Verify it disappears from the list

If any step fails, check:
- Frontend console/network tab for failed requests or wrong base URL
- Backend logs for DB connection errors (DATABASE_URL correctness)
- Confirm CORS allowed origins include http://localhost:3000
- Database is listening at localhost:5000 and has the "notes" table

## 6) OpenAPI regeneration (optional)

If you change routes/models, regenerate the OpenAPI file:
  cd notes_backend
  python -m src.api.generate_openapi

The output updates: notes_backend/interfaces/openapi.json

## Notes

- ID Type Mismatch:
  The backend currently uses integer IDs in SQL queries and Pydantic models.
  The notes_database schema uses UUID ids by default (schema.sql).
  For a seamless smoke test without DB changes, ensure your actual DB table uses integer serial IDs:

  Example quick schema (SQL):
    CREATE TABLE IF NOT EXISTS public.notes (
      id SERIAL PRIMARY KEY,
      title TEXT NOT NULL,
      content TEXT NOT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );

  Alternatively, you can refactor the backend to use UUIDs consistently.

- Allowed origins:
  To allow multiple origins, set ALLOWED_ORIGINS env var:
    ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"

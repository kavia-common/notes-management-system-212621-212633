# notes-management-system-212621-212633

Notes Backend (FastAPI) for the Notes app.

Key defaults:
- Port: 3001 (when you run uvicorn manually)
- CORS allowed origins: http://localhost:3000 (override via ALLOWED_ORIGINS env var)
- DATABASE_URL default: postgresql://appuser:dbuser123@localhost:5000/myapp (override via env)

See INTEGRATION_SMOKETEST.md for end-to-end run and validation steps.
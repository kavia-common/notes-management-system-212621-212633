from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.config import get_settings
from src.api.routers.notes import router as notes_router

app = FastAPI(
    title="Notes Backend API",
    description="REST API for managing notes in the Notes app.",
    version="0.1.0",
    openapi_tags=[
        {"name": "Health", "description": "Service health endpoints"},
        {"name": "Notes", "description": "CRUD operations for notes"},
    ],
)

# Configure CORS to allow http://localhost:3000 by default (can be overridden by env)
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """Health check endpoint to verify the service is running."""
    return {"message": "Healthy"}

# Mount notes router under /api
app.include_router(notes_router, prefix="/api")

import os
from functools import lru_cache

# PUBLIC_INTERFACE
class Settings:
    """Application settings loaded from environment variables.

    Attributes:
        DATABASE_URL: PostgreSQL connection string. If not provided, a sensible
            default pointing to localhost is used.
        ALLOWED_ORIGINS: CORS allowed origins list.
    """
    def __init__(self) -> None:
        # Use provided DATABASE_URL or fall back to a localhost default.
        # NOTE: Do NOT hardcode in code when deploying; override via environment.
        self.DATABASE_URL: str = os.getenv(
            "DATABASE_URL",
            "postgresql://appuser:dbuser123@localhost:5000/myapp",
        )
        # Allow localhost:3000 as requested, can be overridden by env comma list
        origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
        self.ALLOWED_ORIGINS = [o.strip() for o in origins_env.split(",") if o.strip()]


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached Settings instance."""
    return Settings()

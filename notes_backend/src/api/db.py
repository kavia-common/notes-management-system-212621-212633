from contextlib import contextmanager
from typing import Optional, Sequence, Any

import psycopg2
import psycopg2.extras

from src.api.config import get_settings


# PUBLIC_INTERFACE
@contextmanager
def get_connection():
    """Yield a psycopg2 connection based on DATABASE_URL settings.

    Ensures the connection is closed after use.
    """
    settings = get_settings()
    conn = psycopg2.connect(settings.DATABASE_URL)
    try:
        yield conn
    finally:
        try:
            conn.close()
        except Exception:
            # Best-effort close
            pass


# PUBLIC_INTERFACE
@contextmanager
def get_cursor(commit: bool = False):
    """Yield a dict cursor within a managed connection.

    Args:
        commit: Whether to commit the transaction on successful exit.

    Yields:
        A cursor that returns rows as dictionaries (DictCursor).
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            try:
                yield cur
                if commit:
                    conn.commit()
            except Exception:
                conn.rollback()
                raise


# PUBLIC_INTERFACE
def fetch_one(query: str, params: Optional[Sequence[Any]] = None) -> Optional[dict]:
    """Execute a SELECT that returns a single row as dict, or None."""
    with get_cursor() as cur:
        cur.execute(query, params or [])
        row = cur.fetchone()
        return dict(row) if row else None


# PUBLIC_INTERFACE
def fetch_all(query: str, params: Optional[Sequence[Any]] = None) -> list[dict]:
    """Execute a SELECT that returns all rows as list of dicts."""
    with get_cursor() as cur:
        cur.execute(query, params or [])
        rows = cur.fetchall()
        return [dict(r) for r in rows]


# PUBLIC_INTERFACE
def execute(query: str, params: Optional[Sequence[Any]] = None) -> int:
    """Execute an INSERT/UPDATE/DELETE and return affected rowcount."""
    with get_cursor(commit=True) as cur:
        cur.execute(query, params or [])
        return cur.rowcount


# PUBLIC_INTERFACE
def execute_returning(query: str, params: Optional[Sequence[Any]] = None) -> Optional[dict]:
    """Execute a statement with RETURNING and return first row as dict."""
    with get_cursor(commit=True) as cur:
        cur.execute(query, params or [])
        row = cur.fetchone()
        return dict(row) if row else None

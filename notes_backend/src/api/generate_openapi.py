import json
import os

from src.api.main import app

def main():
    """
    Generate OpenAPI schema file under notes_backend/interfaces/openapi.json.

    Run from the repository root or from notes_backend:
        python -m src.api.generate_openapi
    """
    openapi_schema = app.openapi()
    # Resolve output path relative to this file to avoid CWD issues
    here = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # points to notes_backend
    output_dir = os.path.join(here, "interfaces")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "openapi.json")
    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"OpenAPI schema written to {output_path}")

if __name__ == "__main__":
    main()

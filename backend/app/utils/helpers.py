import os
import uuid
import re
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {
    "csv": "text/csv",
    "tiff": "image/tiff",
    "tif": "image/tiff",
    "hdf5": "application/x-hdf5",
    "h5": "application/x-hdf5",
    "bam": "application/octet-stream",
    "json": "application/json",
}

MAX_FILE_SIZES = {
    "imaging": 500 * 1024 * 1024,   # 500 MB
    "crispr": 50 * 1024 * 1024,     # 50 MB
    "tnseq": 200 * 1024 * 1024,     # 200 MB
    "metadata": 10 * 1024 * 1024,   # 10 MB
}


def generate_unique_filename() -> str:
    """Generate a UUID-based filename with no user-supplied data."""
    return str(uuid.uuid4())


def ensure_upload_dir(upload_base: str, *sub_parts: str) -> Path:
    """Create and return a subdirectory under upload_base.

    All sub_parts must be plain names with no path separators.
    Raises ValueError if the resolved path escapes the base.
    """
    base = Path(upload_base).resolve()
    allowed_chars_pattern = re.compile(r'^[a-zA-Z0-9_\-]+$')
    for part in sub_parts:
        if not allowed_chars_pattern.match(str(part)):
            raise ValueError(f"Unsafe path component: {part!r}")
    path = (base.joinpath(*sub_parts)).resolve()
    if not str(path).startswith(str(base)):
        raise ValueError(f"Upload path escapes base directory: {path}")
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower().lstrip(".")


def validate_file_extension(filename: str, allowed: List[str]) -> bool:
    ext = get_file_extension(filename)
    return ext in allowed


def safe_json_loads(data: Optional[str]) -> Any:
    if not data:
        return None
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return None


def safe_json_dumps(data: Any) -> Optional[str]:
    if data is None:
        return None
    try:
        return json.dumps(data)
    except (TypeError, ValueError):
        return None


def paginate(query_result: List[Any], page: int, per_page: int) -> Dict[str, Any]:
    total = len(query_result)
    start = (page - 1) * per_page
    end = start + per_page
    items = query_result[start:end]
    pages = (total + per_page - 1) // per_page
    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
    }

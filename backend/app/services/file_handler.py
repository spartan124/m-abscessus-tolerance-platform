import csv
import io
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {
    "imaging": ["tiff", "tif", "hdf5", "h5"],
    "crispr": ["csv"],
    "tnseq": ["csv", "bam"],
    "metadata": ["json", "csv"],
}


class FileHandler:
    """Handles file validation and basic parsing."""

    def validate_extension(self, filename: str, file_type: str) -> bool:
        ext = Path(filename).suffix.lower().lstrip(".")
        return ext in ALLOWED_EXTENSIONS.get(file_type, [])

    def parse_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse a CSV file and return list of row dicts."""
        rows = []
        try:
            with open(file_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(dict(row))
        except Exception as e:
            logger.error(f"CSV parse error for {file_path}: {e}")
            raise
        return rows

    def parse_csv_from_bytes(self, content: bytes) -> List[Dict[str, Any]]:
        """Parse CSV from bytes."""
        text = content.decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))
        return [dict(row) for row in reader]

    def get_csv_columns(self, file_path: str) -> List[str]:
        """Get column names from CSV."""
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return reader.fieldnames or []

    def detect_file_type(self, filename: str) -> Optional[str]:
        """Detect upload type from filename extension."""
        ext = Path(filename).suffix.lower().lstrip(".")
        if ext in ["tiff", "tif", "hdf5", "h5"]:
            return "imaging"
        if ext == "bam":
            return "tnseq"
        if ext in ["csv", "json"]:
            return "metadata"
        return None

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Process TIFF and HDF5 imaging files."""

    def extract_tiff_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata from TIFF file."""
        try:
            from PIL import Image
            img = Image.open(file_path)
            metadata = {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.size[0],
                "height": img.size[1],
                "n_frames": getattr(img, "n_frames", 1),
            }
            # Try to get TIFF tag metadata
            if hasattr(img, "tag_v2"):
                tag_data = {}
                for k, v in img.tag_v2.items():
                    try:
                        tag_data[str(k)] = str(v)
                    except Exception:
                        pass
                metadata["tags"] = tag_data
            return metadata
        except ImportError:
            logger.warning("Pillow not installed, using mock metadata")
            return self._mock_tiff_metadata(file_path)
        except Exception as e:
            logger.error(f"Error extracting TIFF metadata: {e}")
            return {"error": str(e)}

    def extract_hdf5_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata from HDF5 file."""
        try:
            import h5py
            with h5py.File(file_path, "r") as f:
                metadata = {
                    "keys": list(f.keys()),
                    "attrs": dict(f.attrs),
                }
            return metadata
        except ImportError:
            logger.warning("h5py not installed, using mock metadata")
            return self._mock_hdf5_metadata(file_path)
        except Exception as e:
            logger.error(f"Error extracting HDF5 metadata: {e}")
            return {"error": str(e)}

    def calculate_cell_viability(
        self,
        channel_data: Any,
        live_threshold: float = 0.5,
    ) -> Dict[str, Any]:
        """Calculate cell viability from fluorescent channel data."""
        try:
            import numpy as np
            arr = np.array(channel_data)
            total_cells = int((arr > 0).sum())
            live_cells = int((arr > live_threshold * arr.max()).sum()) if arr.max() > 0 else 0
            dead_cells = total_cells - live_cells
            viability = live_cells / total_cells if total_cells > 0 else 0.0
            return {
                "total_cells": total_cells,
                "live_cells": live_cells,
                "dead_cells": dead_cells,
                "viability_percent": round(viability * 100, 2),
            }
        except ImportError:
            return {"total_cells": 0, "live_cells": 0, "dead_cells": 0, "viability_percent": 0.0}

    def generate_survival_timeseries(
        self, viability_per_timepoint: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate survival curve data from per-timepoint viability."""
        time_points = []
        survival_fractions = []
        for entry in viability_per_timepoint:
            time_points.append(entry.get("time", 0))
            survival_fractions.append(entry.get("viability_percent", 100.0) / 100.0)
        return {
            "time_points": time_points,
            "survival_fractions": survival_fractions,
            "type": "survival_curve",
        }

    def _mock_tiff_metadata(self, file_path: str) -> Dict[str, Any]:
        return {
            "format": "TIFF",
            "mode": "L",
            "size": [512, 512],
            "width": 512,
            "height": 512,
            "n_frames": 1,
            "mock": True,
        }

    def _mock_hdf5_metadata(self, file_path: str) -> Dict[str, Any]:
        return {
            "keys": ["data", "metadata"],
            "attrs": {"description": "Mock HDF5"},
            "mock": True,
        }

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class CrisprProcessor:
    """Process and analyze CRISPRi knockdown screen data."""

    REQUIRED_COLUMNS = ["gene", "guide_rna", "score"]

    def validate_columns(self, columns: List[str]) -> bool:
        lower_cols = [c.lower() for c in columns]
        return all(req in lower_cols for req in self.REQUIRED_COLUMNS)

    def normalize_scores(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Z-score normalize CRISPRi scores."""
        try:
            import numpy as np
            scores = []
            for row in rows:
                try:
                    scores.append(float(row.get("score", 0)))
                except (ValueError, TypeError):
                    scores.append(0.0)

            arr = np.array(scores, dtype=float)
            mean = arr.mean()
            std = arr.std()
            normalized = ((arr - mean) / std).tolist() if std > 0 else [0.0] * len(scores)

            normalized_rows = []
            for i, row in enumerate(rows):
                new_row = dict(row)
                new_row["normalized_score"] = round(normalized[i], 4)
                normalized_rows.append(new_row)
            return normalized_rows
        except ImportError:
            for row in rows:
                row["normalized_score"] = float(row.get("score", 0))
            return rows

    def calculate_log_fold_change(
        self, rows: List[Dict[str, Any]], control_col: str = "control", treatment_col: str = "treatment"
    ) -> List[Dict[str, Any]]:
        """Calculate log2 fold change between treatment and control."""
        try:
            import numpy as np
            result = []
            for row in rows:
                try:
                    ctrl = float(row.get(control_col, 1)) + 1e-10
                    treat = float(row.get(treatment_col, 1)) + 1e-10
                    lfc = float(np.log2(treat / ctrl))
                except (ValueError, TypeError):
                    lfc = 0.0
                new_row = dict(row)
                new_row["log2_fold_change"] = round(lfc, 4)
                result.append(new_row)
            return result
        except ImportError:
            import math
            for row in rows:
                try:
                    ctrl = float(row.get(control_col, 1)) + 1e-10
                    treat = float(row.get(treatment_col, 1)) + 1e-10
                    row["log2_fold_change"] = round(math.log2(treat / ctrl), 4)
                except Exception:
                    row["log2_fold_change"] = 0.0
            return rows

    def filter_hits(
        self,
        rows: List[Dict[str, Any]],
        score_col: str = "normalized_score",
        threshold: float = 2.0,
    ) -> List[Dict[str, Any]]:
        """Filter rows to return hits above threshold (absolute value)."""
        hits = []
        for row in rows:
            try:
                val = abs(float(row.get(score_col, 0)))
                if val >= threshold:
                    hits.append(row)
            except (ValueError, TypeError):
                pass
        return hits

    def aggregate_by_gene(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aggregate guide RNA scores by gene (mean)."""
        gene_scores: Dict[str, List[float]] = {}
        for row in rows:
            gene = row.get("gene", "unknown")
            try:
                score = float(row.get("normalized_score", row.get("score", 0)))
            except (ValueError, TypeError):
                score = 0.0
            gene_scores.setdefault(gene, []).append(score)

        result = []
        for gene, scores in gene_scores.items():
            mean_score = sum(scores) / len(scores)
            result.append({
                "gene": gene,
                "mean_score": round(mean_score, 4),
                "n_guides": len(scores),
            })
        result.sort(key=lambda x: abs(x["mean_score"]), reverse=True)
        return result

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Full processing pipeline for a CRISPRi CSV file."""
        from app.services.file_handler import FileHandler
        handler = FileHandler()
        rows = handler.parse_csv(file_path)
        if not rows:
            return {"error": "Empty file", "hits": [], "summary": {}}

        rows = self.normalize_scores(rows)
        hits = self.filter_hits(rows)
        gene_summary = self.aggregate_by_gene(rows)

        return {
            "total_guides": len(rows),
            "hits": hits,
            "top_genes": gene_summary[:20],
            "summary": {
                "total_guides": len(rows),
                "total_hits": len(hits),
                "top_gene": gene_summary[0]["gene"] if gene_summary else None,
            },
        }

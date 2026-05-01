import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TnseqProcessor:
    """Process transposon mutagenesis (Tn-seq) data."""

    REQUIRED_COLUMNS = ["position", "gene", "read_count"]

    def validate_columns(self, columns: List[str]) -> bool:
        lower_cols = [c.lower() for c in columns]
        return all(req in lower_cols for req in self.REQUIRED_COLUMNS)

    def normalize_by_library_size(
        self, rows: List[Dict[str, Any]], total_reads: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Normalize read counts by library size (RPM)."""
        if total_reads is None:
            total_reads = sum(
                int(r.get("read_count", 0)) for r in rows
                if str(r.get("read_count", "")).isdigit()
            )
        if total_reads == 0:
            return rows

        result = []
        for row in rows:
            new_row = dict(row)
            try:
                rc = float(row.get("read_count", 0))
                new_row["rpm"] = round(rc / total_reads * 1_000_000, 4)
            except (ValueError, TypeError):
                new_row["rpm"] = 0.0
            result.append(new_row)
        return result

    def call_essential_genes(
        self,
        rows: List[Dict[str, Any]],
        rpm_threshold: float = 10.0,
    ) -> List[Dict[str, Any]]:
        """Call genes as essential if RPM below threshold (underrepresented)."""
        gene_rpms: Dict[str, List[float]] = {}
        for row in rows:
            gene = row.get("gene", "unknown")
            try:
                rpm = float(row.get("rpm", row.get("read_count", 0)))
            except (ValueError, TypeError):
                rpm = 0.0
            gene_rpms.setdefault(gene, []).append(rpm)

        essential = []
        for gene, rpms in gene_rpms.items():
            mean_rpm = sum(rpms) / len(rpms)
            is_essential = mean_rpm < rpm_threshold
            essential.append({
                "gene": gene,
                "mean_rpm": round(mean_rpm, 4),
                "insertion_sites": len(rpms),
                "is_essential": is_essential,
            })
        essential.sort(key=lambda x: x["mean_rpm"])
        return essential

    def identify_fitness_hits(
        self,
        rows: List[Dict[str, Any]],
        fold_change_threshold: float = 2.0,
    ) -> List[Dict[str, Any]]:
        """Identify fitness hits by fold-change from control."""
        hits = []
        for row in rows:
            try:
                fc = abs(float(row.get("fold_change", 1.0)))
                if fc >= fold_change_threshold:
                    hits.append(row)
            except (ValueError, TypeError):
                pass
        return hits

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Full processing pipeline for a Tn-seq CSV file."""
        from app.services.file_handler import FileHandler
        handler = FileHandler()
        rows = handler.parse_csv(file_path)
        if not rows:
            return {"error": "Empty file", "essential_genes": [], "summary": {}}

        rows = self.normalize_by_library_size(rows)
        essential = self.call_essential_genes(rows)
        hits = [g for g in essential if g["is_essential"]]

        return {
            "total_insertion_sites": len(rows),
            "essential_genes": hits,
            "all_genes": essential,
            "summary": {
                "total_sites": len(rows),
                "total_genes": len(essential),
                "essential_count": len(hits),
            },
        }

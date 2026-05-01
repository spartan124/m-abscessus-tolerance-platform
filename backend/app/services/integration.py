import logging
from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

logger = logging.getLogger(__name__)


class IntegrationService:
    """Multi-omics data integration service."""

    def __init__(self, mongo_db: AsyncIOMotorDatabase):
        self.mongo = mongo_db

    async def run_integration(
        self, request: Any, db: AsyncSession
    ) -> Dict[str, Any]:
        """Integrate CRISPRi, Tn-seq, and imaging data."""
        from app.models.result import FileUpload
        from app.services.crispr_processor import CrisprProcessor
        from app.services.tnseq_processor import TnseqProcessor

        result_doc: Dict[str, Any] = {
            "experiment_id": request.experiment_id,
            "type": "integration",
            "crispr_hits": [],
            "tnseq_hits": [],
            "convergent_genes": [],
            "summary": {},
        }

        if request.crispr_upload_id:
            res = await db.execute(
                select(FileUpload).where(FileUpload.id == request.crispr_upload_id)
            )
            upload = res.scalar_one_or_none()
            if upload:
                proc = CrisprProcessor()
                crispr_data = proc.process_file(upload.file_path)
                result_doc["crispr_hits"] = [
                    g["gene"] for g in crispr_data.get("top_genes", [])
                    if abs(g.get("mean_score", 0)) >= request.correlation_threshold
                ]

        if request.tnseq_upload_id:
            res = await db.execute(
                select(FileUpload).where(FileUpload.id == request.tnseq_upload_id)
            )
            upload = res.scalar_one_or_none()
            if upload:
                proc = TnseqProcessor()
                tnseq_data = proc.process_file(upload.file_path)
                result_doc["tnseq_hits"] = [
                    g["gene"] for g in tnseq_data.get("essential_genes", [])
                ]

        # Find convergent hits
        crispr_set = set(result_doc["crispr_hits"])
        tnseq_set = set(result_doc["tnseq_hits"])
        result_doc["convergent_genes"] = list(crispr_set & tnseq_set)
        result_doc["summary"] = {
            "crispr_hits": len(crispr_set),
            "tnseq_hits": len(tnseq_set),
            "convergent_genes": len(result_doc["convergent_genes"]),
        }

        # Store in MongoDB
        insert_result = await self.mongo["integration_results"].insert_one(result_doc)
        result_doc["_id"] = str(insert_result.inserted_id)

        # Cache visualization
        await self.mongo["visualization_cache"].update_one(
            {"experiment_id": request.experiment_id, "type": "network"},
            {"$set": {
                "experiment_id": request.experiment_id,
                "type": "network",
                "nodes": [{"id": g, "type": "gene"} for g in result_doc["convergent_genes"]],
                "edges": [],
            }},
            upsert=True,
        )

        return result_doc

    async def run_correlation(
        self, request: Any, db: AsyncSession
    ) -> Dict[str, Any]:
        """Run correlation analysis between two datasets."""
        from app.models.result import FileUpload
        from app.services.file_handler import FileHandler

        handler = FileHandler()
        correlation_data: Dict[str, Any] = {
            "method": request.method,
            "x_upload_id": request.x_upload_id,
            "y_upload_id": request.y_upload_id,
            "correlation": None,
            "pvalue": None,
        }

        try:
            res_x = await db.execute(
                select(FileUpload).where(FileUpload.id == request.x_upload_id)
            )
            res_y = await db.execute(
                select(FileUpload).where(FileUpload.id == request.y_upload_id)
            )
            upload_x = res_x.scalar_one_or_none()
            upload_y = res_y.scalar_one_or_none()

            if not upload_x or not upload_y:
                return correlation_data

            rows_x = handler.parse_csv(upload_x.file_path)
            rows_y = handler.parse_csv(upload_y.file_path)

            if rows_x and rows_y:
                import numpy as np
                from scipy import stats

                scores_x = []
                scores_y = []
                for rx, ry in zip(rows_x, rows_y):
                    try:
                        scores_x.append(float(list(rx.values())[1]))
                        scores_y.append(float(list(ry.values())[1]))
                    except (ValueError, TypeError, IndexError):
                        pass

                if len(scores_x) >= 3:
                    if request.method == "spearman":
                        corr, pval = stats.spearmanr(scores_x, scores_y)
                    else:
                        corr, pval = stats.pearsonr(scores_x, scores_y)
                    correlation_data["correlation"] = round(float(corr), 4)
                    correlation_data["pvalue"] = float(pval)

        except Exception as e:
            logger.error(f"Correlation analysis error: {e}")
            correlation_data["error"] = "Correlation analysis failed"

        return correlation_data

    async def run_pathway_enrichment(self, request: Any) -> Dict[str, Any]:
        """Run Fisher's exact test pathway enrichment."""
        try:
            from scipy import stats

            gene_list = set(request.gene_list)
            background = set(request.background_list or [])
            if not background:
                background = gene_list  # fallback

            # Mock pathway database for MVP
            pathways = {
                "cell_wall_synthesis": {"fabI", "kasA", "embB", "inhA"},
                "dna_repair": {"recA", "lexA", "uvrA", "uvrB"},
                "stress_response": {"groEL", "groES", "dnaK", "clpB"},
                "antibiotic_resistance": {"erm41", "aac", "blaMAB"},
                "energy_metabolism": {"atpA", "atpB", "ndhA"},
            }

            results = []
            for pathway, genes in pathways.items():
                overlap = gene_list & genes
                contingency = [
                    [len(overlap), len(gene_list - genes)],
                    [len(genes - gene_list), len(background - gene_list - genes)],
                ]
                _, pval = stats.fisher_exact(contingency)
                results.append({
                    "pathway": pathway,
                    "overlap_genes": list(overlap),
                    "overlap_count": len(overlap),
                    "pathway_size": len(genes),
                    "pvalue": float(pval),
                    "significant": pval < request.pvalue_cutoff,
                })

            results.sort(key=lambda x: x["pvalue"])
            return {"pathways": results, "gene_count": len(gene_list)}

        except ImportError:
            return {
                "pathways": [],
                "gene_count": len(request.gene_list),
                "error": "scipy not installed",
            }
        except Exception as e:
            logger.error(f"Pathway enrichment error: {e}")
            return {"pathways": [], "error": "Pathway enrichment analysis failed"}

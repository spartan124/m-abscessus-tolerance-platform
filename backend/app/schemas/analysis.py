from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class IntegrationRequest(BaseModel):
    experiment_id: int
    crispr_upload_id: Optional[int] = None
    tnseq_upload_id: Optional[int] = None
    imaging_upload_id: Optional[int] = None
    correlation_threshold: float = 0.5
    pvalue_cutoff: float = 0.05


class CorrelationRequest(BaseModel):
    experiment_id: int
    x_upload_id: int
    y_upload_id: int
    method: str = "pearson"  # pearson, spearman


class PathwayEnrichmentRequest(BaseModel):
    experiment_id: int
    gene_list: List[str]
    background_list: Optional[List[str]] = None
    pvalue_cutoff: float = 0.05


class AnalysisResultResponse(BaseModel):
    id: int
    experiment_id: int
    result_type: str
    name: str
    description: Optional[str] = None
    mongo_id: Optional[str] = None
    summary: Optional[Dict[str, Any]] = None
    created_at: str
    model_config = {"from_attributes": True}

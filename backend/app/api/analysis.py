import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db, get_mongo_db
from app.models.experiment import Experiment
from app.models.result import FileUpload, Result, ResultType
from app.models.user import User
from app.schemas.analysis import (
    IntegrationRequest, CorrelationRequest,
    PathwayEnrichmentRequest, AnalysisResultResponse,
)
from app.security import get_current_user
from app.services.integration import IntegrationService
from app.services.crispr_processor import CrisprProcessor
from app.services.tnseq_processor import TnseqProcessor

router = APIRouter()


@router.post("/integrate")
async def run_integration(
    request: IntegrationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exp_result = await db.execute(
        select(Experiment).where(Experiment.id == request.experiment_id)
    )
    exp = exp_result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    if exp.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    mongo_db = get_mongo_db()
    service = IntegrationService(mongo_db)
    result_doc = await service.run_integration(request, db)

    result = Result(
        experiment_id=request.experiment_id,
        result_type=ResultType.INTEGRATION,
        name=f"Integration result for experiment {request.experiment_id}",
        mongo_id=result_doc.get("_id"),
        summary_json=json.dumps(result_doc.get("summary", {})),
    )
    db.add(result)
    await db.flush()
    return {"result_id": result.id, "summary": result_doc.get("summary", {})}


@router.get("/results/{experiment_id}", response_model=List[AnalysisResultResponse])
async def get_results(
    experiment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exp_result = await db.execute(
        select(Experiment).where(Experiment.id == experiment_id)
    )
    exp = exp_result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    if exp.owner_id != current_user.id and not exp.is_public and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    result = await db.execute(
        select(Result).where(Result.experiment_id == experiment_id)
    )
    results = result.scalars().all()

    response = []
    for r in results:
        summary = json.loads(r.summary_json) if r.summary_json else None
        response.append(
            AnalysisResultResponse(
                id=r.id,
                experiment_id=r.experiment_id,
                result_type=r.result_type,
                name=r.name,
                description=r.description,
                mongo_id=r.mongo_id,
                summary=summary,
                created_at=r.created_at.isoformat(),
            )
        )
    return response


@router.post("/correlate")
async def run_correlation(
    request: CorrelationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exp_result = await db.execute(
        select(Experiment).where(Experiment.id == request.experiment_id)
    )
    if not exp_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Experiment not found")

    # Load upload files
    for uid in [request.x_upload_id, request.y_upload_id]:
        res = await db.execute(select(FileUpload).where(FileUpload.id == uid))
        if not res.scalar_one_or_none():
            raise HTTPException(status_code=404, detail=f"Upload {uid} not found")

    mongo_db = get_mongo_db()
    service = IntegrationService(mongo_db)
    correlation_result = await service.run_correlation(request, db)
    return correlation_result


@router.get("/genotype-phenotype/{experiment_id}")
async def get_genotype_phenotype(
    experiment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mongo_db = get_mongo_db()
    doc = await mongo_db["visualization_cache"].find_one(
        {"experiment_id": experiment_id, "type": "genotype_phenotype"}
    )
    if not doc:
        raise HTTPException(status_code=404, detail="No genotype-phenotype data available")
    doc["_id"] = str(doc["_id"])
    return doc


@router.post("/pathway-enrichment/{experiment_id}")
async def pathway_enrichment(
    experiment_id: int,
    request: PathwayEnrichmentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mongo_db = get_mongo_db()
    service = IntegrationService(mongo_db)
    result = await service.run_pathway_enrichment(request)
    return result

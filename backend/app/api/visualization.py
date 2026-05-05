from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db, get_mongo_db
from app.models.experiment import Experiment
from app.models.user import User
from app.security import get_current_user

router = APIRouter()


async def _check_experiment_access(
    experiment_id: int, db: AsyncSession, current_user: User
) -> Experiment:
    result = await db.execute(
        select(Experiment).where(Experiment.id == experiment_id)
    )
    exp = result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    if exp.owner_id != current_user.id and not exp.is_public and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return exp


@router.get("/survival-curve/{experiment_id}")
async def get_survival_curve(
    experiment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _check_experiment_access(experiment_id, db, current_user)
    mongo_db = get_mongo_db()
    doc = await mongo_db["visualization_cache"].find_one(
        {"experiment_id": experiment_id, "type": "survival_curve"}
    )
    if not doc:
        raise HTTPException(status_code=404, detail="No survival curve data available")
    doc["_id"] = str(doc["_id"])
    return doc


@router.get("/heatmap/{experiment_id}")
async def get_heatmap(
    experiment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _check_experiment_access(experiment_id, db, current_user)
    mongo_db = get_mongo_db()
    doc = await mongo_db["visualization_cache"].find_one(
        {"experiment_id": experiment_id, "type": "heatmap"}
    )
    if not doc:
        raise HTTPException(status_code=404, detail="No heatmap data available")
    doc["_id"] = str(doc["_id"])
    return doc


@router.get("/time-kill/{experiment_id}")
async def get_time_kill(
    experiment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _check_experiment_access(experiment_id, db, current_user)
    mongo_db = get_mongo_db()
    doc = await mongo_db["visualization_cache"].find_one(
        {"experiment_id": experiment_id, "type": "time_kill"}
    )
    if not doc:
        raise HTTPException(status_code=404, detail="No time-kill data available")
    doc["_id"] = str(doc["_id"])
    return doc


@router.get("/scatter/{experiment_id}")
async def get_scatter(
    experiment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _check_experiment_access(experiment_id, db, current_user)
    mongo_db = get_mongo_db()
    doc = await mongo_db["visualization_cache"].find_one(
        {"experiment_id": experiment_id, "type": "scatter"}
    )
    if not doc:
        raise HTTPException(status_code=404, detail="No scatter plot data available")
    doc["_id"] = str(doc["_id"])
    return doc


@router.get("/images/{experiment_id}")
async def get_image_metadata(
    experiment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _check_experiment_access(experiment_id, db, current_user)
    mongo_db = get_mongo_db()
    cursor = mongo_db["imaging_results"].find({"experiment_id": experiment_id})
    docs = await cursor.to_list(length=100)
    for doc in docs:
        doc["_id"] = str(doc["_id"])
    return {"images": docs, "total": len(docs)}


@router.get("/network/{experiment_id}")
async def get_network(
    experiment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await _check_experiment_access(experiment_id, db, current_user)
    mongo_db = get_mongo_db()
    doc = await mongo_db["visualization_cache"].find_one(
        {"experiment_id": experiment_id, "type": "network"}
    )
    if not doc:
        raise HTTPException(status_code=404, detail="No network data available")
    doc["_id"] = str(doc["_id"])
    return doc

import math
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from app.database import get_db
from app.models.experiment import Experiment, ExperimentType, ExperimentStatus
from app.models.strain import Strain
from app.models.drug import Drug
from app.models.condition import Condition
from app.models.user import User
from app.schemas.experiment import (
    ExperimentCreate, ExperimentUpdate, ExperimentResponse, ExperimentListResponse,
    StrainCreate, StrainResponse, DrugCreate, DrugResponse,
    ConditionCreate, ConditionResponse,
)
from app.security import get_current_user

router = APIRouter()


# ---- Strains ----
@router.get("/strains", response_model=List[StrainResponse])
async def list_strains(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Strain))
    return result.scalars().all()


@router.post("/strains", response_model=StrainResponse, status_code=201)
async def create_strain(data: StrainCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Strain).where(Strain.name == data.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Strain name already exists")
    strain = Strain(**data.model_dump())
    db.add(strain)
    await db.flush()
    await db.refresh(strain)
    return strain


# ---- Drugs ----
@router.get("/drugs", response_model=List[DrugResponse])
async def list_drugs(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Drug))
    return result.scalars().all()


@router.post("/drugs", response_model=DrugResponse, status_code=201)
async def create_drug(data: DrugCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Drug).where(Drug.name == data.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Drug name already exists")
    drug = Drug(**data.model_dump())
    db.add(drug)
    await db.flush()
    await db.refresh(drug)
    return drug


# ---- Conditions ----
@router.get("/conditions", response_model=List[ConditionResponse])
async def list_conditions(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Condition))
    return result.scalars().all()


@router.post("/conditions", response_model=ConditionResponse, status_code=201)
async def create_condition(data: ConditionCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Condition).where(Condition.name == data.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Condition name already exists")
    condition = Condition(**data.model_dump())
    db.add(condition)
    await db.flush()
    await db.refresh(condition)
    return condition


# ---- Experiments ----
@router.get("/", response_model=ExperimentListResponse)
async def list_experiments(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    experiment_type: Optional[ExperimentType] = Query(None),
    status: Optional[ExperimentStatus] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Experiment).where(
        or_(Experiment.owner_id == current_user.id, Experiment.is_public == True)
    )
    if search:
        query = query.where(
            or_(
                Experiment.name.ilike(f"%{search}%"),
                Experiment.description.ilike(f"%{search}%"),
            )
        )
    if experiment_type:
        query = query.where(Experiment.experiment_type == experiment_type)
    if status:
        query = query.where(Experiment.status == status)

    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar_one()

    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    experiments = result.scalars().all()

    return ExperimentListResponse(
        experiments=experiments,
        total=total,
        page=page,
        per_page=per_page,
        pages=math.ceil(total / per_page) if total > 0 else 0,
    )


@router.post("/", response_model=ExperimentResponse, status_code=201)
async def create_experiment(
    data: ExperimentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    experiment = Experiment(**data.model_dump(), owner_id=current_user.id)
    db.add(experiment)
    await db.flush()
    await db.refresh(experiment)
    return experiment


@router.get("/{experiment_id}", response_model=ExperimentResponse)
async def get_experiment(
    experiment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Experiment).where(Experiment.id == experiment_id)
    )
    exp = result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    if exp.owner_id != current_user.id and not exp.is_public and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return exp


@router.put("/{experiment_id}", response_model=ExperimentResponse)
async def update_experiment(
    experiment_id: int,
    data: ExperimentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Experiment).where(Experiment.id == experiment_id))
    exp = result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    if exp.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(exp, field, value)
    await db.flush()
    await db.refresh(exp)
    return exp


@router.delete("/{experiment_id}", status_code=204)
async def delete_experiment(
    experiment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Experiment).where(Experiment.id == experiment_id))
    exp = result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    if exp.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    await db.delete(exp)


@router.get("/{experiment_id}/summary")
async def get_experiment_summary(
    experiment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Experiment).where(Experiment.id == experiment_id))
    exp = result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    if exp.owner_id != current_user.id and not exp.is_public and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return {
        "id": exp.id,
        "name": exp.name,
        "type": exp.experiment_type,
        "status": exp.status,
        "uploads": len(exp.file_uploads),
        "results": len(exp.results),
        "created_at": exp.created_at.isoformat(),
    }

import os
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database import get_db
from app.models.experiment import Experiment
from app.models.result import FileUpload
from app.models.user import User
from app.schemas.upload import UploadResponse, UploadStatusResponse
from app.security import get_current_user
from app.services.file_handler import FileHandler

router = APIRouter()


async def _save_upload(
    experiment_id: int,
    file: UploadFile,
    file_type: str,
    db: AsyncSession,
    current_user: User,
) -> FileUpload:
    # Verify experiment access
    exp_result = await db.execute(
        select(Experiment).where(Experiment.id == experiment_id)
    )
    exp = exp_result.scalar_one_or_none()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    if exp.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    # Validate extension against known allowlist for this file_type
    handler = FileHandler()
    if not handler.validate_extension(file.filename, file_type):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type for {file_type} upload",
        )

    # Build upload directory entirely from trusted (non-user) sources:
    #   - settings.UPLOAD_DIR: server configuration
    #   - exp.id: database-returned integer (not raw form input)
    #   - file_type: hardcoded per route, not user-supplied
    upload_base = Path(settings.UPLOAD_DIR).resolve()
    upload_dir = (upload_base / str(exp.id) / file_type).resolve()
    if not str(upload_dir).startswith(str(upload_base)):
        raise HTTPException(status_code=400, detail="Invalid upload path")
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Filename is a pure UUID — no user-supplied data in the stored path
    unique_name = str(uuid.uuid4())
    file_path = upload_dir / unique_name

    file_bytes = await file.read()
    file_size = len(file_bytes)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    record = FileUpload(
        experiment_id=exp.id,
        filename=unique_name,
        original_filename=file.filename,
        file_type=file_type,
        file_size=file_size,
        file_path=str(file_path),
        mime_type=file.content_type,
        status="uploaded",
    )
    db.add(record)
    await db.flush()
    await db.refresh(record)
    return record


@router.post("/imaging", response_model=UploadResponse, status_code=201)
async def upload_imaging(
    experiment_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await _save_upload(experiment_id, file, "imaging", db, current_user)


@router.post("/crispr", response_model=UploadResponse, status_code=201)
async def upload_crispr(
    experiment_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await _save_upload(experiment_id, file, "crispr", db, current_user)


@router.post("/tnseq", response_model=UploadResponse, status_code=201)
async def upload_tnseq(
    experiment_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await _save_upload(experiment_id, file, "tnseq", db, current_user)


@router.post("/metadata", response_model=UploadResponse, status_code=201)
async def upload_metadata(
    experiment_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await _save_upload(experiment_id, file, "metadata", db, current_user)


@router.get("/status/{upload_id}", response_model=UploadStatusResponse)
async def get_upload_status(
    upload_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(FileUpload).where(FileUpload.id == upload_id))
    upload = result.scalar_one_or_none()
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")
    return upload

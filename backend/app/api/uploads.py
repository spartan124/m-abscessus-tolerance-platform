import os
import shutil
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
from app.utils.helpers import generate_unique_filename, ensure_upload_dir

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

    # Validate extension
    handler = FileHandler()
    if not handler.validate_extension(file.filename, file_type):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type for {file_type} upload",
        )

    # Save file
    upload_dir = ensure_upload_dir(
        os.path.join(settings.UPLOAD_DIR, str(experiment_id), file_type),
        base_dir=settings.UPLOAD_DIR,
    )
    unique_name = generate_unique_filename(file.filename)
    file_path = (upload_dir / unique_name).resolve()

    # Guard against path traversal
    base = Path(settings.UPLOAD_DIR).resolve()
    if not str(file_path).startswith(str(base)):
        raise HTTPException(status_code=400, detail="Invalid file path")

    file_bytes = await file.read()
    file_size = len(file_bytes)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    record = FileUpload(
        experiment_id=experiment_id,
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

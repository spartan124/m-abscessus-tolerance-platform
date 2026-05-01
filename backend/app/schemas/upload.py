from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: int
    experiment_id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    status: str
    mongo_result_id: Optional[str] = None
    created_at: datetime
    model_config = {"from_attributes": True}


class UploadStatusResponse(BaseModel):
    id: int
    status: str
    processing_log: Optional[str] = None
    mongo_result_id: Optional[str] = None
    updated_at: datetime
    model_config = {"from_attributes": True}

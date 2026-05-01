from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.models.experiment import ExperimentStatus, ExperimentType


class StrainBase(BaseModel):
    name: str
    subspecies: Optional[str] = None
    genotype: Optional[str] = None
    source: Optional[str] = None
    description: Optional[str] = None
    is_clinical_isolate: bool = False
    clinical_metadata: Optional[str] = None


class StrainCreate(StrainBase):
    pass


class StrainResponse(StrainBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class DrugBase(BaseModel):
    name: str
    drug_class: Optional[str] = None
    mechanism: Optional[str] = None
    mic_reference: Optional[float] = None
    mic_unit: str = "µg/mL"
    description: Optional[str] = None


class DrugCreate(DrugBase):
    pass


class DrugResponse(DrugBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class ConditionBase(BaseModel):
    name: str
    temperature_celsius: Optional[float] = None
    ph: Optional[float] = None
    oxygen_level: Optional[str] = None
    media: Optional[str] = None
    supplements: Optional[str] = None
    description: Optional[str] = None


class ConditionCreate(ConditionBase):
    pass


class ConditionResponse(ConditionBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}


class ExperimentBase(BaseModel):
    name: str
    description: Optional[str] = None
    experiment_type: ExperimentType
    is_public: bool = False
    strain_id: Optional[int] = None
    drug_id: Optional[int] = None
    condition_id: Optional[int] = None
    drug_concentration: Optional[float] = None
    drug_concentration_unit: Optional[str] = None
    time_points: Optional[str] = None
    replicates: int = 1
    notes: Optional[str] = None
    tags: Optional[str] = None


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ExperimentStatus] = None
    is_public: Optional[bool] = None
    strain_id: Optional[int] = None
    drug_id: Optional[int] = None
    condition_id: Optional[int] = None
    drug_concentration: Optional[float] = None
    drug_concentration_unit: Optional[str] = None
    time_points: Optional[str] = None
    replicates: Optional[int] = None
    notes: Optional[str] = None
    tags: Optional[str] = None


class ExperimentResponse(ExperimentBase):
    id: int
    owner_id: int
    status: ExperimentStatus
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class ExperimentListResponse(BaseModel):
    experiments: List[ExperimentResponse]
    total: int
    page: int
    per_page: int
    pages: int

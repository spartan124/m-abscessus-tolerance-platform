from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import (
    Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ExperimentStatus(str, PyEnum):
    CREATED = "created"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ExperimentType(str, PyEnum):
    IMAGING = "imaging"
    CRISPR = "crispr"
    TNSEQ = "tnseq"
    INTEGRATED = "integrated"


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    experiment_type: Mapped[ExperimentType] = mapped_column(
        Enum(ExperimentType), nullable=False
    )
    status: Mapped[ExperimentStatus] = mapped_column(
        Enum(ExperimentStatus), default=ExperimentStatus.CREATED
    )
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)

    # Foreign keys
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    strain_id: Mapped[int] = mapped_column(ForeignKey("strains.id"), nullable=True)
    drug_id: Mapped[int] = mapped_column(ForeignKey("drugs.id"), nullable=True)
    condition_id: Mapped[int] = mapped_column(ForeignKey("conditions.id"), nullable=True)

    # Experiment parameters
    drug_concentration: Mapped[float] = mapped_column(Float, nullable=True)
    drug_concentration_unit: Mapped[str] = mapped_column(String(20), nullable=True)
    time_points: Mapped[str] = mapped_column(Text, nullable=True)  # JSON: [0, 1, 4, 24, 48]
    replicates: Mapped[int] = mapped_column(Integer, default=1)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    tags: Mapped[str] = mapped_column(String(500), nullable=True)  # comma-separated

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="experiments")
    strain: Mapped["Strain"] = relationship("Strain", back_populates="experiments")
    drug: Mapped["Drug"] = relationship("Drug", back_populates="experiments")
    condition: Mapped["Condition"] = relationship("Condition", back_populates="experiments")
    file_uploads: Mapped[list] = relationship("FileUpload", back_populates="experiment", lazy="select")
    results: Mapped[list] = relationship("Result", back_populates="experiment", lazy="select")

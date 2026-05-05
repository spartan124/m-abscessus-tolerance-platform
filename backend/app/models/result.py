from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ResultType(str, PyEnum):
    SURVIVAL_CURVE = "survival_curve"
    TIME_KILL = "time_kill"
    HEATMAP = "heatmap"
    SCATTER = "scatter"
    CORRELATION = "correlation"
    GENOTYPE_PHENOTYPE = "genotype_phenotype"
    PATHWAY_ENRICHMENT = "pathway_enrichment"
    INTEGRATION = "integration"


class FileUpload(Base):
    __tablename__ = "file_uploads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)  # imaging, crispr, tnseq, metadata
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)  # bytes
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="uploaded")  # uploaded, processing, processed, failed
    processing_log: Mapped[str] = mapped_column(Text, nullable=True)
    mongo_result_id: Mapped[str] = mapped_column(String(100), nullable=True)  # MongoDB document ID
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    experiment: Mapped["Experiment"] = relationship("Experiment", back_populates="file_uploads")


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"), nullable=False)
    result_type: Mapped[ResultType] = mapped_column(Enum(ResultType), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    mongo_id: Mapped[str] = mapped_column(String(100), nullable=True)  # MongoDB document ID for large data
    summary_json: Mapped[str] = mapped_column(Text, nullable=True)  # small summary as JSON
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    experiment: Mapped["Experiment"] = relationship("Experiment", back_populates="results")

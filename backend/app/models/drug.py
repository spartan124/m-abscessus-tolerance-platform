from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Drug(Base):
    __tablename__ = "drugs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    drug_class: Mapped[str] = mapped_column(String(100), nullable=True)  # aminoglycoside, macrolide, etc.
    mechanism: Mapped[str] = mapped_column(Text, nullable=True)
    mic_reference: Mapped[float] = mapped_column(Float, nullable=True)  # reference MIC µg/mL
    mic_unit: Mapped[str] = mapped_column(String(20), default="µg/mL")
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    experiments: Mapped[list] = relationship("Experiment", back_populates="drug", lazy="select")

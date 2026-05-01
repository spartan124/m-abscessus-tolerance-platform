from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Condition(Base):
    __tablename__ = "conditions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    temperature_celsius: Mapped[float] = mapped_column(Float, nullable=True)
    ph: Mapped[float] = mapped_column(Float, nullable=True)
    oxygen_level: Mapped[str] = mapped_column(String(50), nullable=True)  # aerobic, microaerobic, anaerobic
    media: Mapped[str] = mapped_column(String(255), nullable=True)  # 7H9, LB, etc.
    supplements: Mapped[str] = mapped_column(Text, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    experiments: Mapped[list] = relationship("Experiment", back_populates="condition", lazy="select")

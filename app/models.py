from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Index,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Measurement(Base):
    __tablename__ = "measurement"
    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    value = Column(Float)
    place = Column(String(50))
    record_id = Column(Integer, ForeignKey("record.id"))
    record = relationship("Record")
    __table_args__ = (Index("idx_rec_id_place", "record_id", "place"),)


class Record(Base):
    __tablename__ = "record"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, index=True)
    time_sync = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    measurement = relationship("Measurement")

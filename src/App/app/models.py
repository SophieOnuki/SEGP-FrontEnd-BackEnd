from sqlalchemy import Column, Integer, String, ForeignKey, Enum, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app import Base

class File(Base):
    __tablename__ = 'files'

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(255), nullable=False)
    file_type = Column(Enum("RGB-D", "Depth"), nullable=False)
    upload_date = Column(TIMESTAMP, default=func.now())

    predictions = relationship("Prediction", back_populates="file")

class Prediction(Base):
    __tablename__ = 'predictions'

    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey('files.file_id', ondelete='CASCADE'), nullable=False)
    mass_prediction = Column(DECIMAL(10,2), nullable=False)
    model_version = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

    file = relationship("File", back_populates="predictions")


class ExportedData(Base):
    __tablename__ = 'exporteddata'

    csv_id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey('files.file_id', ondelete='CASCADE'), nullable=False)
    csv_path = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
"""Database models for digital twin health project."""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Patient(Base):
    """Patient model for storing patient information."""
    
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(String(10))
    email = Column(String(100), unique=True, nullable=True)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vitals = relationship("VitalSigns", back_populates="patient", cascade="all, delete-orphan")
    predictions = relationship("HealthPrediction", back_populates="patient", cascade="all, delete-orphan")


class VitalSigns(Base):
    """Vital signs model for storing patient health metrics."""
    
    __tablename__ = "vital_signs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    heart_rate = Column(Float, nullable=False)
    bmi = Column(Float, nullable=False)
    bp_systolic = Column(Float, nullable=False)
    bp_diastolic = Column(Float, nullable=False)
    oxygen_saturation = Column(Float, nullable=False)
    respiratory_rate = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="vitals")


class HealthPrediction(Base):
    """Health prediction results model."""
    
    __tablename__ = "health_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    prediction_type = Column(String(100), nullable=False)
    prediction_value = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    risk_level = Column(String(50))  # e.g., "low", "medium", "high"
    recommendations = Column(Text, nullable=True)
    prediction_timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="predictions")


class ModelMetadata(Base):
    """Model metadata for tracking LoRA model versions."""
    
    __tablename__ = "model_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False, unique=True)
    model_version = Column(String(50), nullable=False)
    lora_rank = Column(Integer, default=8)
    lora_alpha = Column(Integer, default=16)
    checkpoint_path = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=False)
    accuracy = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

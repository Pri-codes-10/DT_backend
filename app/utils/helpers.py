"""Utility functions and helpers."""

import logging
from datetime import datetime
from typing import Dict, Any
import json

logger = logging.getLogger(__name__)


def setup_logging(log_file: str, log_level: str = "INFO") -> None:
    """
    Setup application logging.
    
    Args:
        log_file: Path to log file
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )


def format_response(data: Any, message: str = "Success", status: str = "success") -> Dict[str, Any]:
    """
    Format API response.
    
    Args:
        data: Response data
        message: Status message
        status: Status type (success, error, warning)
        
    Returns:
        Formatted response dictionary
    """
    return {
        "status": status,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat(),
    }


def calculate_patient_age(date_of_birth: datetime) -> int:
    """
    Calculate patient age from date of birth.
    
    Args:
        date_of_birth: Patient's date of birth
        
    Returns:
        Age in years
    """
    today = datetime.utcnow()
    age = today.year - date_of_birth.year
    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        age -= 1
    return age


def validate_vital_signs(vitals: Dict[str, float]) -> tuple[bool, str]:
    """
    Validate vital signs are within reasonable ranges.
    
    Args:
        vitals: Dictionary of vital signs
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    ranges = {
        "heart_rate": (40, 200),
        "temperature": (35, 42),
        "bp_systolic": (70, 200),
        "bp_diastolic": (40, 130),
        "oxygen_saturation": (70, 100),
        "respiratory_rate": (8, 40),
    }
    
    for vital, (min_val, max_val) in ranges.items():
        if vital in vitals:
            value = vitals[vital]
            if not (min_val <= value <= max_val):
                return False, f"{vital} {value} is outside normal range ({min_val}-{max_val})"
    
    return True, "Valid"


import os

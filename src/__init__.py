"""
Churn Prediction Package
Machine Learning system for predicting customer churn in telecom industry
"""

__version__ = "0.1.0"
__author__ = "Churn Prediction Team"

from .config import get_config
from .logger import get_logger, setup_logger
from .data_validation import DataValidator

__all__ = [
    'get_config',
    'get_logger',
    'setup_logger',
    'DataValidator',
]

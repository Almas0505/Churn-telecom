"""
Test configuration and fixtures for pytest
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path


@pytest.fixture
def sample_raw_data():
    """Sample raw data for testing"""
    return pd.DataFrame({
        'customerID': ['C001', 'C002', 'C003'],
        'gender': ['Male', 'Female', 'Male'],
        'SeniorCitizen': [0, 1, 0],
        'Partner': ['Yes', 'No', 'Yes'],
        'Dependents': ['No', 'Yes', 'No'],
        'tenure': [12, 24, 6],
        'PhoneService': ['Yes', 'Yes', 'No'],
        'MultipleLines': ['No', 'Yes', 'No phone service'],
        'InternetService': ['Fiber optic', 'DSL', 'No'],
        'OnlineSecurity': ['No', 'Yes', 'No internet service'],
        'OnlineBackup': ['No', 'Yes', 'No internet service'],
        'DeviceProtection': ['Yes', 'No', 'No internet service'],
        'TechSupport': ['No', 'Yes', 'No internet service'],
        'StreamingTV': ['Yes', 'No', 'No internet service'],
        'StreamingMovies': ['Yes', 'Yes', 'No internet service'],
        'Contract': ['Month-to-month', 'One year', 'Two year'],
        'PaperlessBilling': ['Yes', 'No', 'Yes'],
        'PaymentMethod': ['Electronic check', 'Mailed check', 'Bank transfer'],
        'MonthlyCharges': [70.5, 55.2, 20.0],
        'TotalCharges': ['846.0', '1324.8', '120.0'],
        'Churn': ['Yes', 'No', 'No']
    })


@pytest.fixture
def sample_processed_data():
    """Sample processed data for testing"""
    return pd.DataFrame({
        'tenure': [12, 24, 6],
        'MonthlyCharges': [70.5, 55.2, 20.0],
        'TotalCharges': [846.0, 1324.8, 120.0],
        'SeniorCitizen': [0, 1, 0],
        'Partner': [1, 0, 1],
        'Dependents': [0, 1, 0],
        'PhoneService': [1, 1, 0],
        'PaperlessBilling': [1, 0, 1],
        'Churn': ['Yes', 'No', 'No']
    })


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create temporary data directory"""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "raw").mkdir()
    (data_dir / "processed").mkdir()
    return data_dir


@pytest.fixture
def temp_models_dir(tmp_path):
    """Create temporary models directory"""
    models_dir = tmp_path / "models"
    models_dir.mkdir()
    return models_dir

"""
Unit tests for features module
"""
import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from features import (
    create_tenure_group,
    create_avg_monthly_spend,
    create_total_services,
    create_has_internet,
    create_has_support,
    create_price_per_service,
    engineer_features,
    encode_binary_features,
    encode_categorical_features
)


class TestCreateTenureGroup:
    def test_tenure_group_creation(self, sample_processed_data):
        """Test tenure group creation"""
        df = create_tenure_group(sample_processed_data)
        
        assert 'tenure_group' in df.columns
        assert df['tenure_group'].dtype.name == 'category'
        
    def test_tenure_group_labels(self):
        """Test tenure group labels"""
        df = pd.DataFrame({'tenure': [6, 18, 30, 60]})
        result = create_tenure_group(df)
        
        expected_labels = ['0-1 year', '1-2 years', '2-4 years', '4+ years']
        assert all(result['tenure_group'].cat.categories == expected_labels)


class TestCreateAvgMonthlySpend:
    def test_avg_monthly_spend_calculation(self):
        """Test average monthly spend calculation"""
        df = pd.DataFrame({
            'TotalCharges': [1200.0, 500.0],
            'tenure': [12, 10]
        })
        
        result = create_avg_monthly_spend(df)
        
        assert 'avg_monthly_spend' in result.columns
        assert result['avg_monthly_spend'].iloc[0] == pytest.approx(1200.0 / 13, rel=1e-2)
        
    def test_avg_monthly_spend_no_division_by_zero(self):
        """Test that division by zero is handled"""
        df = pd.DataFrame({
            'TotalCharges': [100.0],
            'tenure': [0]
        })
        
        result = create_avg_monthly_spend(df)
        
        assert result['avg_monthly_spend'].iloc[0] == 100.0


class TestCreateTotalServices:
    def test_total_services_count(self):
        """Test total services counting"""
        df = pd.DataFrame({
            'PhoneService': ['Yes', 'No', 'Yes'],
            'InternetService': ['Fiber optic', 'No', 'DSL'],
            'OnlineSecurity': ['Yes', 'No', 'No'],
            'OnlineBackup': ['No', 'No', 'Yes'],
            'DeviceProtection': ['No', 'No', 'No'],
            'TechSupport': ['Yes', 'No', 'No'],
            'StreamingTV': ['No', 'No', 'Yes'],
            'StreamingMovies': ['Yes', 'No', 'No'],
            'MultipleLines': ['No', 'No', 'Yes']
        })
        
        result = create_total_services(df)
        
        assert 'total_services' in result.columns
        assert result['total_services'].iloc[0] == 4  # PhoneService, OnlineSecurity, TechSupport, StreamingMovies
        assert result['total_services'].iloc[1] == 0  # All No


class TestCreateHasInternet:
    def test_has_internet_flag(self):
        """Test internet service flag creation"""
        df = pd.DataFrame({
            'InternetService': ['Fiber optic', 'DSL', 'No', 'Fiber optic']
        })
        
        result = create_has_internet(df)
        
        assert 'has_internet' in result.columns
        assert result['has_internet'].tolist() == [1, 1, 0, 1]


class TestCreateHasSupport:
    def test_has_support_flag(self):
        """Test support services flag creation"""
        df = pd.DataFrame({
            'OnlineSecurity': ['Yes', 'No', 'No', 'Yes'],
            'TechSupport': ['No', 'Yes', 'No', 'No'],
            'DeviceProtection': ['No', 'No', 'Yes', 'No']
        })
        
        result = create_has_support(df)
        
        assert 'has_support' in result.columns
        assert result['has_support'].tolist() == [1, 1, 1, 1]


class TestCreatePricePerService:
    def test_price_per_service_calculation(self):
        """Test price per service calculation"""
        df = pd.DataFrame({
            'MonthlyCharges': [100.0, 50.0],
            'total_services': [4, 0]
        })
        
        result = create_price_per_service(df)
        
        assert 'price_per_service' in result.columns
        assert result['price_per_service'].iloc[0] == pytest.approx(100.0 / 5, rel=1e-2)
        assert result['price_per_service'].iloc[1] == pytest.approx(50.0, rel=1e-2)


class TestEngineerFeatures:
    def test_engineer_features_pipeline(self):
        """Test full feature engineering pipeline"""
        df = pd.DataFrame({
            'tenure': [12, 24],
            'MonthlyCharges': [70.0, 55.0],
            'TotalCharges': [840.0, 1320.0],
            'PhoneService': ['Yes', 'No'],
            'InternetService': ['Fiber optic', 'DSL'],
            'OnlineSecurity': ['Yes', 'No'],
            'OnlineBackup': ['No', 'Yes'],
            'DeviceProtection': ['No', 'No'],
            'TechSupport': ['Yes', 'No'],
            'StreamingTV': ['No', 'Yes'],
            'StreamingMovies': ['Yes', 'No'],
            'MultipleLines': ['No', 'No']
        })
        
        result = engineer_features(df)
        
        # Check all new features are created
        assert 'tenure_group' in result.columns
        assert 'avg_monthly_spend' in result.columns
        assert 'total_services' in result.columns
        assert 'has_internet' in result.columns
        assert 'has_support' in result.columns
        assert 'price_per_service' in result.columns


class TestEncodeBinaryFeatures:
    def test_encode_binary_features(self):
        """Test binary feature encoding"""
        df = pd.DataFrame({
            'Partner': ['Yes', 'No', 'Yes'],
            'Dependents': ['No', 'Yes', 'No'],
            'PhoneService': ['Yes', 'Yes', 'No'],
            'PaperlessBilling': ['Yes', 'No', 'Yes']
        })
        
        result = encode_binary_features(df)
        
        assert result['Partner'].tolist() == [1, 0, 1]
        assert result['Dependents'].tolist() == [0, 1, 0]
        assert result['PhoneService'].tolist() == [1, 1, 0]
        assert result['PaperlessBilling'].tolist() == [1, 0, 1]


class TestEncodeCategoricalFeatures:
    def test_encode_categorical_features(self):
        """Test one-hot encoding of categorical features"""
        df = pd.DataFrame({
            'Contract': ['Month-to-month', 'One year', 'Two year'],
            'InternetService': ['Fiber optic', 'DSL', 'No'],
            'Churn': ['Yes', 'No', 'No']
        })
        
        result = encode_categorical_features(df)
        
        # Check Churn is not encoded
        assert 'Churn' in result.columns
        assert result['Churn'].dtype == object
        
        # Check categorical features are one-hot encoded
        assert 'Contract_One year' in result.columns or 'Contract_Two year' in result.columns
        assert 'InternetService_DSL' in result.columns or 'InternetService_Fiber optic' in result.columns
        
    def test_encode_categorical_drop_first(self):
        """Test drop_first parameter"""
        df = pd.DataFrame({
            'Contract': ['Month-to-month', 'One year', 'Two year'],
            'Churn': ['Yes', 'No', 'No']
        })
        
        result = encode_categorical_features(df, drop_first=False)
        
        # With drop_first=False, all categories should be present
        assert 'Contract_Month-to-month' in result.columns
        assert 'Contract_One year' in result.columns
        assert 'Contract_Two year' in result.columns

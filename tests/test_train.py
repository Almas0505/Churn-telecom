"""
Unit tests for train module
"""
import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from train import (
    split_data,
    scale_features,
    balance_data,
    train_model
)


class TestSplitData:
    def test_split_data_shapes(self):
        """Test data splitting shapes"""
        df = pd.DataFrame({
            'feature1': range(100),
            'feature2': range(100, 200),
            'Churn': ['Yes' if i % 2 == 0 else 'No' for i in range(100)]
        })
        
        X_train, X_test, y_train, y_test = split_data(df, test_size=0.2)
        
        assert len(X_train) == 80
        assert len(X_test) == 20
        assert len(y_train) == 80
        assert len(y_test) == 20
        
    def test_split_data_target_encoding(self):
        """Test that target is properly encoded"""
        df = pd.DataFrame({
            'feature1': range(10),
            'Churn': ['Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No']
        })
        
        X_train, X_test, y_train, y_test = split_data(df)
        
        assert set(y_train.unique()).issubset({0, 1})
        assert set(y_test.unique()).issubset({0, 1})
        
    def test_split_data_stratification(self):
        """Test stratified split maintains class distribution"""
        df = pd.DataFrame({
            'feature1': range(100),
            'Churn': ['Yes'] * 30 + ['No'] * 70
        })
        
        X_train, X_test, y_train, y_test = split_data(df, test_size=0.2)
        
        # Check proportions are roughly maintained
        train_ratio = y_train.sum() / len(y_train)
        test_ratio = y_test.sum() / len(y_test)
        
        assert abs(train_ratio - 0.3) < 0.1
        assert abs(test_ratio - 0.3) < 0.1


class TestScaleFeatures:
    def test_scale_features_output_type(self):
        """Test that scaling returns DataFrames"""
        X_train = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [10, 20, 30]})
        X_test = pd.DataFrame({'feature1': [4, 5], 'feature2': [40, 50]})
        
        X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
        
        assert isinstance(X_train_scaled, pd.DataFrame)
        assert isinstance(X_test_scaled, pd.DataFrame)
        
    def test_scale_features_preserves_shape(self):
        """Test that scaling preserves data shape"""
        X_train = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [10, 20, 30]})
        X_test = pd.DataFrame({'feature1': [4, 5], 'feature2': [40, 50]})
        
        X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
        
        assert X_train_scaled.shape == X_train.shape
        assert X_test_scaled.shape == X_test.shape
        
    def test_scale_features_standardization(self):
        """Test that features are standardized"""
        X_train = pd.DataFrame({'feature1': [1, 2, 3, 4, 5]})
        X_test = pd.DataFrame({'feature1': [6]})
        
        X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
        
        # Check mean is close to 0 and std is close to 1
        assert abs(X_train_scaled['feature1'].mean()) < 1e-10
        assert abs(X_train_scaled['feature1'].std() - 1.0) < 0.1


class TestBalanceData:
    def test_balance_data_increases_minority_class(self):
        """Test that SMOTE increases minority class samples"""
        X_train = pd.DataFrame({
            'feature1': list(range(100)),
            'feature2': list(range(100, 200))
        })
        y_train = pd.Series([0] * 80 + [1] * 20)
        
        X_balanced, y_balanced = balance_data(X_train, y_train)
        
        # After SMOTE, classes should be balanced
        assert len(X_balanced) > len(X_train)
        assert (y_balanced == 0).sum() == (y_balanced == 1).sum()
        
    def test_balance_data_preserves_features(self):
        """Test that features are preserved after balancing"""
        X_train = pd.DataFrame({
            'feature1': list(range(100)),
            'feature2': list(range(100, 200))
        })
        y_train = pd.Series([0] * 80 + [1] * 20)
        
        X_balanced, y_balanced = balance_data(X_train, y_train)
        
        assert list(X_balanced.columns) == list(X_train.columns)


class TestTrainModel:
    def test_train_model_xgboost(self):
        """Test XGBoost model training"""
        X_train = pd.DataFrame(np.random.rand(50, 5))
        y_train = pd.Series([0, 1] * 25)
        
        model = train_model(X_train, y_train, model_type='xgboost')
        
        assert hasattr(model, 'predict')
        assert hasattr(model, 'predict_proba')
        
    def test_train_model_random_forest(self):
        """Test Random Forest model training"""
        X_train = pd.DataFrame(np.random.rand(50, 5))
        y_train = pd.Series([0, 1] * 25)
        
        model = train_model(X_train, y_train, model_type='random_forest')
        
        assert hasattr(model, 'predict')
        assert hasattr(model, 'predict_proba')
        
    def test_train_model_gradient_boosting(self):
        """Test Gradient Boosting model training"""
        X_train = pd.DataFrame(np.random.rand(50, 5))
        y_train = pd.Series([0, 1] * 25)
        
        model = train_model(X_train, y_train, model_type='gradient_boosting')
        
        assert hasattr(model, 'predict')
        assert hasattr(model, 'predict_proba')
        
    def test_train_model_predictions(self):
        """Test that trained model can make predictions"""
        X_train = pd.DataFrame(np.random.rand(50, 5))
        y_train = pd.Series([0, 1] * 25)
        
        model = train_model(X_train, y_train, model_type='xgboost')
        
        predictions = model.predict(X_train)
        
        assert len(predictions) == len(X_train)
        assert set(predictions).issubset({0, 1})
        
    def test_train_model_invalid_type(self):
        """Test error handling for invalid model type"""
        X_train = pd.DataFrame(np.random.rand(50, 5))
        y_train = pd.Series([0, 1] * 25)
        
        with pytest.raises(ValueError, match="Unknown model_type"):
            train_model(X_train, y_train, model_type='invalid_model')

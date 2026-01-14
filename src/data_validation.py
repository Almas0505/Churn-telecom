"""
Data validation module
Validates data quality and schema
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path


class DataValidator:
    """Validator for churn prediction data"""
    
    # Expected schema for raw data
    REQUIRED_COLUMNS = [
        'customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents',
        'tenure', 'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
        'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
        'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn'
    ]
    
    NUMERIC_COLUMNS = ['tenure', 'MonthlyCharges', 'SeniorCitizen']
    
    CATEGORICAL_COLUMNS = [
        'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
        'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
        'PaperlessBilling', 'PaymentMethod', 'Churn'
    ]
    
    def __init__(self):
        """Initialize validator"""
        self.validation_errors = []
        self.validation_warnings = []
    
    def validate_schema(self, df: pd.DataFrame) -> bool:
        """
        Validate that DataFrame has required columns
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if schema is valid, False otherwise
        """
        missing_cols = set(self.REQUIRED_COLUMNS) - set(df.columns)
        
        if missing_cols:
            error_msg = f"Missing required columns: {missing_cols}"
            self.validation_errors.append(error_msg)
            return False
        
        return True
    
    def validate_data_types(self, df: pd.DataFrame) -> bool:
        """
        Validate data types of columns
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if data types are valid, False otherwise
        """
        is_valid = True
        
        # Check numeric columns
        for col in self.NUMERIC_COLUMNS:
            if col in df.columns:
                # Check if can be converted to numeric
                try:
                    pd.to_numeric(df[col], errors='coerce')
                except Exception as e:
                    error_msg = f"Column '{col}' cannot be converted to numeric: {e}"
                    self.validation_errors.append(error_msg)
                    is_valid = False
        
        return is_valid
    
    def validate_ranges(self, df: pd.DataFrame) -> bool:
        """
        Validate that numeric values are in expected ranges
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if ranges are valid, False otherwise
        """
        is_valid = True
        
        # Tenure should be non-negative
        if 'tenure' in df.columns:
            if (df['tenure'] < 0).any():
                error_msg = "Negative values found in 'tenure' column"
                self.validation_errors.append(error_msg)
                is_valid = False
        
        # MonthlyCharges should be non-negative
        if 'MonthlyCharges' in df.columns:
            if (df['MonthlyCharges'] < 0).any():
                error_msg = "Negative values found in 'MonthlyCharges' column"
                self.validation_errors.append(error_msg)
                is_valid = False
        
        # TotalCharges validation
        if 'TotalCharges' in df.columns:
            total_charges_numeric = pd.to_numeric(df['TotalCharges'], errors='coerce')
            if (total_charges_numeric < 0).any():
                error_msg = "Negative values found in 'TotalCharges' column"
                self.validation_errors.append(error_msg)
                is_valid = False
        
        return is_valid
    
    def validate_missing_values(self, df: pd.DataFrame, threshold: float = 0.5) -> bool:
        """
        Validate missing values in DataFrame
        
        Args:
            df: DataFrame to validate
            threshold: Maximum allowed proportion of missing values per column
            
        Returns:
            True if missing values are within threshold
        """
        is_valid = True
        
        for col in df.columns:
            missing_ratio = df[col].isnull().sum() / len(df)
            
            if missing_ratio > threshold:
                error_msg = f"Column '{col}' has {missing_ratio:.2%} missing values (threshold: {threshold:.2%})"
                self.validation_errors.append(error_msg)
                is_valid = False
            elif missing_ratio > 0.1:  # Warning threshold
                warning_msg = f"Column '{col}' has {missing_ratio:.2%} missing values"
                self.validation_warnings.append(warning_msg)
        
        return is_valid
    
    def validate_duplicates(self, df: pd.DataFrame) -> bool:
        """
        Check for duplicate customer IDs
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if no duplicates found
        """
        if 'customerID' in df.columns:
            duplicates = df['customerID'].duplicated().sum()
            
            if duplicates > 0:
                warning_msg = f"Found {duplicates} duplicate customer IDs"
                self.validation_warnings.append(warning_msg)
                return False
        
        return True
    
    def validate_categorical_values(self, df: pd.DataFrame) -> bool:
        """
        Validate categorical column values
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if categorical values are valid
        """
        is_valid = True
        
        # Define expected values for key categorical columns
        expected_values = {
            'gender': ['Male', 'Female'],
            'Partner': ['Yes', 'No'],
            'Dependents': ['Yes', 'No'],
            'PhoneService': ['Yes', 'No'],
            'Churn': ['Yes', 'No']
        }
        
        for col, valid_values in expected_values.items():
            if col in df.columns:
                invalid_values = set(df[col].dropna().unique()) - set(valid_values)
                
                if invalid_values:
                    error_msg = f"Column '{col}' has unexpected values: {invalid_values}"
                    self.validation_errors.append(error_msg)
                    is_valid = False
        
        return is_valid
    
    def validate(self, df: pd.DataFrame, skip_schema: bool = False) -> bool:
        """
        Run full validation pipeline
        
        Args:
            df: DataFrame to validate
            skip_schema: Skip schema validation (useful for processed data)
            
        Returns:
            True if all validations pass
        """
        self.validation_errors = []
        self.validation_warnings = []
        
        is_valid = True
        
        # Schema validation
        if not skip_schema:
            is_valid &= self.validate_schema(df)
        
        # Data type validation
        is_valid &= self.validate_data_types(df)
        
        # Range validation
        is_valid &= self.validate_ranges(df)
        
        # Missing values validation
        is_valid &= self.validate_missing_values(df)
        
        # Duplicates check
        self.validate_duplicates(df)
        
        # Categorical values validation
        if not skip_schema:
            is_valid &= self.validate_categorical_values(df)
        
        return is_valid
    
    def get_validation_report(self) -> Dict[str, Any]:
        """
        Get validation report
        
        Returns:
            Dictionary with validation results
        """
        return {
            'is_valid': len(self.validation_errors) == 0,
            'errors': self.validation_errors,
            'warnings': self.validation_warnings,
            'num_errors': len(self.validation_errors),
            'num_warnings': len(self.validation_warnings)
        }
    
    def print_validation_report(self):
        """Print validation report to console"""
        report = self.get_validation_report()
        
        print("\n" + "="*60)
        print("📋 Data Validation Report")
        print("="*60)
        
        if report['is_valid']:
            print("✅ Validation PASSED")
        else:
            print("❌ Validation FAILED")
        
        if report['errors']:
            print(f"\n🔴 Errors ({report['num_errors']}):")
            for i, error in enumerate(report['errors'], 1):
                print(f"  {i}. {error}")
        
        if report['warnings']:
            print(f"\n⚠️  Warnings ({report['num_warnings']}):")
            for i, warning in enumerate(report['warnings'], 1):
                print(f"  {i}. {warning}")
        
        if not report['errors'] and not report['warnings']:
            print("\n✨ No issues found!")
        
        print("="*60 + "\n")


if __name__ == "__main__":
    # Example usage
    validator = DataValidator()
    
    # Create sample data
    sample_data = pd.DataFrame({
        'customerID': ['C001', 'C002', 'C003'],
        'gender': ['Male', 'Female', 'Male'],
        'SeniorCitizen': [0, 1, 0],
        'Partner': ['Yes', 'No', 'Yes'],
        'Dependents': ['No', 'Yes', 'No'],
        'tenure': [12, 24, -5],  # Invalid: negative tenure
        'PhoneService': ['Yes', 'Yes', 'No'],
        'MultipleLines': ['No', 'Yes', 'No'],
        'InternetService': ['Fiber optic', 'DSL', 'No'],
        'OnlineSecurity': ['No', 'Yes', 'No'],
        'OnlineBackup': ['No', 'Yes', 'No'],
        'DeviceProtection': ['Yes', 'No', 'No'],
        'TechSupport': ['No', 'Yes', 'No'],
        'StreamingTV': ['Yes', 'No', 'No'],
        'StreamingMovies': ['Yes', 'Yes', 'No'],
        'Contract': ['Month-to-month', 'One year', 'Two year'],
        'PaperlessBilling': ['Yes', 'No', 'Yes'],
        'PaymentMethod': ['Electronic check', 'Mailed check', 'Bank transfer'],
        'MonthlyCharges': [70.5, 55.2, 20.0],
        'TotalCharges': ['846.0', '1324.8', '120.0'],
        'Churn': ['Yes', 'No', 'No']
    })
    
    # Validate
    is_valid = validator.validate(sample_data)
    validator.print_validation_report()

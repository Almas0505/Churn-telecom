"""
Unit tests for data_preparation module
"""
import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_preparation import (
    load_raw_data,
    clean_total_charges,
    remove_customer_id,
    prepare_data
)


class TestLoadRawData:
    def test_load_raw_data_success(self, sample_raw_data, temp_data_dir):
        """Test successful data loading"""
        file_path = temp_data_dir / "raw" / "test_data.csv"
        sample_raw_data.to_csv(file_path, index=False)
        
        df = load_raw_data(str(file_path))
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert 'customerID' in df.columns
        
    def test_load_raw_data_file_not_found(self):
        """Test loading non-existent file"""
        with pytest.raises(FileNotFoundError):
            load_raw_data('non_existent_file.csv')


class TestCleanTotalCharges:
    def test_clean_total_charges_conversion(self, sample_raw_data):
        """Test TotalCharges conversion to float"""
        df = clean_total_charges(sample_raw_data)
        
        assert df['TotalCharges'].dtype == float
        
    def test_clean_total_charges_no_nulls(self, sample_raw_data):
        """Test that nulls are filled"""
        # Add a row with empty TotalCharges
        sample_raw_data.loc[3] = ['C004', 'Male', 0, 'Yes', 'No', 0, 'Yes', 'No',
                                    'No', 'No', 'No', 'No', 'No', 'No', 'No',
                                    'Month-to-month', 'Yes', 'Electronic check',
                                    50.0, '', 'No']
        
        df = clean_total_charges(sample_raw_data)
        
        assert df['TotalCharges'].isnull().sum() == 0
        
    def test_clean_total_charges_fills_with_monthly(self, sample_raw_data):
        """Test that nulls are filled with MonthlyCharges"""
        sample_raw_data.loc[3] = ['C004', 'Male', 0, 'Yes', 'No', 0, 'Yes', 'No',
                                    'No', 'No', 'No', 'No', 'No', 'No', 'No',
                                    'Month-to-month', 'Yes', 'Electronic check',
                                    50.0, '', 'No']
        
        df = clean_total_charges(sample_raw_data)
        
        assert df.loc[3, 'TotalCharges'] == 50.0


class TestRemoveCustomerId:
    def test_remove_customer_id(self, sample_raw_data):
        """Test customerID removal"""
        df = remove_customer_id(sample_raw_data)
        
        assert 'customerID' not in df.columns
        
    def test_remove_customer_id_preserves_other_columns(self, sample_raw_data):
        """Test that other columns are preserved"""
        original_cols = len(sample_raw_data.columns)
        df = remove_customer_id(sample_raw_data)
        
        assert len(df.columns) == original_cols - 1
        

class TestPrepareData:
    def test_prepare_data_pipeline(self, sample_raw_data, temp_data_dir):
        """Test full data preparation pipeline"""
        file_path = temp_data_dir / "raw" / "test_data.csv"
        sample_raw_data.to_csv(file_path, index=False)
        
        df = prepare_data(str(file_path))
        
        assert isinstance(df, pd.DataFrame)
        assert 'customerID' not in df.columns
        assert df['TotalCharges'].dtype == float
        assert df['TotalCharges'].isnull().sum() == 0

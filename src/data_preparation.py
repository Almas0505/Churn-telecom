"""
Data Preparation Module
Функции для загрузки и очистки данных
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_raw_data(file_path: str) -> pd.DataFrame:
    """
    Загрузка сырых данных
    
    Args:
        file_path: Путь к CSV файлу
        
    Returns:
        DataFrame с данными
    """
    df = pd.read_csv(file_path)
    print(f"✅ Данные загружены: {df.shape}")
    return df


def clean_total_charges(df: pd.DataFrame) -> pd.DataFrame:
    """
    Очистка колонки TotalCharges (конвертация в float, обработка пропусков)
    
    Args:
        df: Исходный DataFrame
        
    Returns:
        Очищенный DataFrame
    """
    df = df.copy()
    
    # Конвертируем в float
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # Заполняем пропуски MonthlyCharges (для новых клиентов)
    df['TotalCharges'].fillna(df['MonthlyCharges'], inplace=True)
    
    print(f"✅ TotalCharges очищен. Пропусков: {df['TotalCharges'].isnull().sum()}")
    return df


def remove_customer_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Удаление customerID (не информативен для модели)
    
    Args:
        df: DataFrame
        
    Returns:
        DataFrame без customerID
    """
    df = df.copy()
    if 'customerID' in df.columns:
        df.drop('customerID', axis=1, inplace=True)
        print("✅ customerID удален")
    return df


def prepare_data(file_path: str) -> pd.DataFrame:
    """
    Полный пайплайн подготовки данных
    
    Args:
        file_path: Путь к raw данным
        
    Returns:
        Подготовленный DataFrame
    """
    df = load_raw_data(file_path)
    df = clean_total_charges(df)
    df = remove_customer_id(df)
    
    print(f"✅ Данные подготовлены: {df.shape}")
    return df


if __name__ == "__main__":
    # Пример использования
    df = prepare_data('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    print(df.head())

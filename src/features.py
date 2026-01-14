"""
Feature Engineering Module
Создание новых признаков и преобразование данных
"""

import pandas as pd
import numpy as np


def create_tenure_group(df: pd.DataFrame) -> pd.DataFrame:
    """Создание группы по сроку пользования услугами"""
    df = df.copy()
    df['tenure_group'] = pd.cut(df['tenure'], 
                                bins=[0, 12, 24, 48, 72],
                                labels=['0-1 year', '1-2 years', '2-4 years', '4+ years'])
    return df


def create_avg_monthly_spend(df: pd.DataFrame) -> pd.DataFrame:
    """Средняя стоимость в месяц"""
    df = df.copy()
    df['avg_monthly_spend'] = df['TotalCharges'] / (df['tenure'] + 1)
    return df


def create_total_services(df: pd.DataFrame) -> pd.DataFrame:
    """Подсчет общего количества услуг"""
    df = df.copy()
    services = ['PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
               'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    
    df['total_services'] = 0
    for col in services:
        if col in df.columns:
            df['total_services'] += (df[col] == 'Yes').astype(int)
    
    return df


def create_has_internet(df: pd.DataFrame) -> pd.DataFrame:
    """Флаг наличия интернета"""
    df = df.copy()
    df['has_internet'] = (df['InternetService'] != 'No').astype(int)
    return df


def create_has_support(df: pd.DataFrame) -> pd.DataFrame:
    """Флаг наличия услуг поддержки"""
    df = df.copy()
    df['has_support'] = ((df['OnlineSecurity'] == 'Yes') | 
                        (df['TechSupport'] == 'Yes') |
                        (df['DeviceProtection'] == 'Yes')).astype(int)
    return df


def create_price_per_service(df: pd.DataFrame) -> pd.DataFrame:
    """Цена за услугу"""
    df = df.copy()
    df['price_per_service'] = df['MonthlyCharges'] / (df['total_services'] + 1)
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Полный пайплайн feature engineering
    
    Args:
        df: DataFrame с базовыми признаками
        
    Returns:
        DataFrame с новыми признаками
    """
    df = create_tenure_group(df)
    df = create_avg_monthly_spend(df)
    df = create_total_services(df)
    df = create_has_internet(df)
    df = create_has_support(df)
    df = create_price_per_service(df)
    
    print(f"✅ Feature Engineering завершен. Размер: {df.shape}")
    return df


def encode_binary_features(df: pd.DataFrame) -> pd.DataFrame:
    """Бинарное кодирование Yes/No колонок"""
    df = df.copy()
    binary_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
    
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].map({'Yes': 1, 'No': 0})
    
    print(f"✅ Бинарное кодирование применено к {len(binary_cols)} колонкам")
    return df


def encode_categorical_features(df: pd.DataFrame, drop_first: bool = True) -> pd.DataFrame:
    """One-Hot Encoding категориальных признаков"""
    df = df.copy()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Удаляем target если есть
    if 'Churn' in categorical_cols:
        categorical_cols.remove('Churn')
    
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=drop_first)
    print(f"✅ One-Hot Encoding завершен. Размер: {df.shape}")
    return df


if __name__ == "__main__":
    # Пример использования
    from data_preparation import prepare_data
    
    df = prepare_data('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    df = engineer_features(df)
    print(df.head())

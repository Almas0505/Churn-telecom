"""
Model Training Module
Обучение моделей для прогнозирования churn
"""

import pandas as pd
import numpy as np
import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE


def split_data(df: pd.DataFrame, target_col: str = 'Churn', test_size: float = 0.2, random_state: int = 42):
    """
    Разделение данных на train/test
    
    Args:
        df: DataFrame с данными
        target_col: Название целевой переменной
        test_size: Размер test выборки
        random_state: Random seed
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    X = df.drop(target_col, axis=1)
    y = df[target_col].map({'No': 0, 'Yes': 1})
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"✅ Данные разделены: Train {X_train.shape}, Test {X_test.shape}")
    return X_train, X_test, y_train, y_test


def scale_features(X_train: pd.DataFrame, X_test: pd.DataFrame):
    """
    Стандартизация признаков
    
    Args:
        X_train: Train данные
        X_test: Test данные
        
    Returns:
        X_train_scaled, X_test_scaled, scaler
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Конвертируем обратно в DataFrame
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
    
    print(f"✅ Признаки стандартизированы")
    return X_train_scaled, X_test_scaled, scaler


def balance_data(X_train, y_train, random_state: int = 42):
    """
    Балансировка классов с SMOTE
    
    Args:
        X_train: Train данные
        y_train: Train labels
        random_state: Random seed
        
    Returns:
        X_train_balanced, y_train_balanced
    """
    smote = SMOTE(random_state=random_state)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    
    print(f"✅ SMOTE применен. Размер: {X_train_balanced.shape}")
    return X_train_balanced, y_train_balanced


def train_model(X_train, y_train, model_type: str = 'xgboost', random_state: int = 42):
    """
    Обучение модели
    
    Args:
        X_train: Train данные
        y_train: Train labels
        model_type: Тип модели ('xgboost', 'random_forest', 'gradient_boosting')
        random_state: Random seed
        
    Returns:
        Обученная модель
    """
    if model_type == 'xgboost':
        model = XGBClassifier(random_state=random_state, n_estimators=100, 
                            max_depth=5, eval_metric='logloss')
    elif model_type == 'random_forest':
        model = RandomForestClassifier(random_state=random_state, n_estimators=100, max_depth=15)
    elif model_type == 'gradient_boosting':
        model = GradientBoostingClassifier(random_state=random_state, n_estimators=100, max_depth=5)
    else:
        raise ValueError(f"Unknown model_type: {model_type}")
    
    model.fit(X_train, y_train)
    print(f"✅ Модель {model_type} обучена")
    return model


def save_artifacts(model, scaler, feature_names: list, output_dir: str = '../models'):
    """
    Сохранение модели и артефактов
    
    Args:
        model: Обученная модель
        scaler: StandardScaler
        feature_names: Список признаков
        output_dir: Папка для сохранения
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Сохраняем модель
    with open(output_path / 'churn_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Сохраняем scaler
    with open(output_path / 'scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    # Сохраняем feature names
    with open(output_path / 'feature_names.pkl', 'wb') as f:
        pickle.dump(feature_names, f)
    
    print(f"✅ Артефакты сохранены в {output_dir}")


def save_data(X_train, X_test, y_train, y_test, output_dir: str = '../data/processed'):
    """
    Сохранение train и test данных
    
    Args:
        X_train: Train признаки
        X_test: Test признаки
        y_train: Train метки
        y_test: Test метки
        output_dir: Папка для сохранения
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Сохраняем train данные
    X_train.to_csv(output_path / 'train.csv', index=False)
    pd.Series(y_train, name='Churn').to_csv(output_path / 'train_labels.csv', index=False)
    
    # Сохраняем test данные
    X_test.to_csv(output_path / 'test.csv', index=False)
    pd.Series(y_test, name='Churn').to_csv(output_path / 'test_labels.csv', index=False)
    
    print(f"✅ Данные сохранены в {output_dir}")


if __name__ == "__main__":
    # Пример использования
    from data_preparation import prepare_data
    from features import engineer_features, encode_binary_features, encode_categorical_features
    
    # Подготовка данных
    df = prepare_data('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    df = engineer_features(df)
    df = encode_binary_features(df)
    df = encode_categorical_features(df)
    
    # Обучение
    X_train, X_test, y_train, y_test = split_data(df)
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    X_train_balanced, y_train_balanced = balance_data(X_train_scaled, y_train)
    
    model = train_model(X_train_balanced, y_train_balanced, model_type='xgboost')
    
    # Сохранение
    save_artifacts(model, scaler, X_train.columns.tolist())
    save_data(X_train_scaled, X_test_scaled, y_train, y_test)

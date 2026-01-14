"""
Model Evaluation Module
Оценка моделей
"""

import pandas as pd
import numpy as np
import pickle
import json
from pathlib import Path

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)


def load_model(model_path: str):
    """Загрузка обученной модели"""
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print(f"✅ Модель загружена: {type(model).__name__}")
    return model


def evaluate_model(model, X_test, y_test):
    """
    Оценка модели
    
    Args:
        model: Обученная модель
        X_test: Test данные
        y_test: Test labels
        
    Returns:
        Словарь с метриками
    """
    # Предсказания
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Метрики
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }
    
    # Вывод результатов
    print("\n" + "="*60)
    print("🎯 Результаты оценки на тестовой выборке")
    print("="*60)
    for metric, value in metrics.items():
        print(f"{metric:12}: {value:.4f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n📊 Confusion Matrix:")
    print(cm)
    
    # Classification Report
    print(f"\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['No Churn', 'Churn']))
    
    return metrics


def save_metrics(metrics: dict, output_path: str = 'reports/metrics.json'):
    """
    Сохранение метрик в JSON
    
    Args:
        metrics: Словарь с метриками
        output_path: Путь для сохранения
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    
    print(f"\n✅ Метрики сохранены: {output_path}")


if __name__ == "__main__":
    # Пример использования
    model = load_model('models/churn_model.pkl')
    
    X_test = pd.read_csv('data/processed/test.csv')
    y_test_df = pd.read_csv('data/processed/test_labels.csv')
    y_test = y_test_df['Churn']
    
    metrics = evaluate_model(model, X_test, y_test)
    save_metrics(metrics)

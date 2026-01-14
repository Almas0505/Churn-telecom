"""
Inference Module
Прогнозирование на новых данных
"""

import pandas as pd
import numpy as np
import pickle
from pathlib import Path


class ChurnPredictor:
    """Класс для прогнозирования churn"""
    
    def __init__(self, model_dir: str = 'models'):
        """
        Инициализация
        
        Args:
            model_dir: Папка с моделью и артефактами
        """
        self.model_dir = Path(model_dir)
        self.model = None
        self.scaler = None
        self.feature_names = None
        
    def load_artifacts(self):
        """Загрузка модели, scaler и feature names"""
        # Модель
        with open(self.model_dir / 'churn_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        
        # Scaler
        with open(self.model_dir / 'scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
        
        # Feature names
        with open(self.model_dir / 'feature_names.pkl', 'rb') as f:
            self.feature_names = pickle.load(f)
        
        print(f"✅ Артефакты загружены: {type(self.model).__name__}")
    
    def preprocess(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Предобработка данных
        
        Args:
            X: DataFrame с признаками
            
        Returns:
            Предобработанный DataFrame
        """
        # Убедимся, что все признаки есть
        missing_features = set(self.feature_names) - set(X.columns)
        if missing_features:
            raise ValueError(f"Отсутствуют признаки: {missing_features}")
        
        # Выбираем только нужные колонки в правильном порядке
        X = X[self.feature_names]
        
        # Стандартизация
        X_scaled = self.scaler.transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
        
        return X_scaled
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Прогнозирование класса (0 или 1)
        
        Args:
            X: DataFrame с признаками
            
        Returns:
            Массив предсказаний (0 или 1)
        """
        if self.model is None:
            self.load_artifacts()
        
        X_processed = self.preprocess(X)
        predictions = self.model.predict(X_processed)
        
        return predictions
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Прогнозирование вероятности churn
        
        Args:
            X: DataFrame с признаками
            
        Returns:
            Массив вероятностей
        """
        if self.model is None:
            self.load_artifacts()
        
        X_processed = self.preprocess(X)
        probabilities = self.model.predict_proba(X_processed)[:, 1]
        
        return probabilities
    
    def predict_with_details(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Прогнозирование с деталями
        
        Args:
            X: DataFrame с признаками
            
        Returns:
            DataFrame с предсказаниями и вероятностями
        """
        predictions = self.predict(X)
        probabilities = self.predict_proba(X)
        
        results = pd.DataFrame({
            'prediction': predictions,
            'churn_probability': probabilities,
            'risk_level': pd.cut(probabilities, bins=[0, 0.3, 0.7, 1.0],
                                labels=['Low', 'Medium', 'High'])
        }, index=X.index)
        
        return results


if __name__ == "__main__":
    # Пример использования
    predictor = ChurnPredictor(model_dir='models')
    predictor.load_artifacts()
    
    # Загрузка тестовых данных
    X_test = pd.read_csv('data/processed/test.csv')
    
    # Прогнозирование
    if len(X_test) > 0:
        results = predictor.predict_with_details(X_test.head(10))
        print("\n✅ Прогнозы:")
        print(results)
    else:
        print("⚠️ Тестовые данные пусты. Запустите train.py сначала.")

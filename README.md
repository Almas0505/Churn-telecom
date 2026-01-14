# 📊 Telco Customer Churn Analysis

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.2-orange)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-brightgreen)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🎯 **Цель проекта**: Предсказание оттока клиентов телекоммуникационной компании с использованием Machine Learning

---

## 📋 Описание

Этот проект представляет собой полноценное end-to-end ML решение для задачи бинарной классификации. Основная цель — построить модель, которая предсказывает вероятность ухода клиента (churn), чтобы компания могла своевременно предпринять меры по их удержанию.

**Датасет**: [IBM Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) (Kaggle)
- 7043 клиента
- 21 признак (демография, услуги, контракты, платежи)
- Целевая переменная: Churn (Yes/No)

---

## 🏗️ Структура проекта

```
telco-churn/
├── README.md                 # Документация проекта
├── requirements.txt          # Зависимости
├── data/
│   ├── raw/                 # Исходные данные
│   └── processed/           # Обработанные данные (train/test)
├── notebooks/
│   ├── 01_eda.ipynb         # Exploratory Data Analysis
│   ├── 02_preprocessing_modeling.ipynb  # Обработка и обучение
│   └── 03_model_evaluation_explainability.ipynb  # Оценка модели
├── src/
│   ├── data_preparation.py  # Загрузка и очистка данных
│   ├── features.py          # Feature engineering
│   ├── train.py             # Обучение модели
│   ├── evaluate.py          # Оценка модели
│   └── inference.py         # Прогнозирование
├── models/
│   ├── churn_model.pkl      # Обученная модель
│   ├── scaler.pkl           # StandardScaler
│   └── feature_names.pkl    # Список признаков
└── reports/
    ├── metrics.json         # Метрики модели
    └── figures/             # Визуализации
```

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/telco-churn.git
cd telco-churn
```

### 2. Установка зависимостей

```bash
# Создание виртуального окружения
python -m venv .venv

# Активация (Windows)
.venv\Scripts\activate

# Активация (Linux/Mac)
source .venv/bin/activate

# Установка пакетов
pip install -r requirements.txt
```

### 3. Загрузка данных

Скачайте датасет с [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) и поместите файл `WA_Fn-UseC_-Telco-Customer-Churn.csv` в папку `data/raw/`.

### 4. Запуск проекта

#### Обучение модели:
```bash
cd src
python train.py
```

#### Оценка модели:
```bash
python evaluate.py
```

#### Прогнозирование:
```bash
python inference.py
```

---

## 📊 Результаты

### Метрики лучшей модели (XGBoost + SMOTE):

| Метрика | Значение |
|---------|----------|
| **Accuracy** | 0.82 |
| **Precision** | 0.68 |
| **Recall** | 0.55 |
| **F1-Score** | 0.61 |
| **ROC-AUC** | 0.85 |

### Ключевые инсайты:

1. **Tenure** (срок пользования) — самый важный признак
2. Клиенты с **month-to-month** контрактами имеют самый высокий churn rate (~42%)
3. **Fiber optic** интернет связан с повышенным оттоком
4. **Electronic check** как метод оплаты коррелирует с churn
5. Применение **SMOTE** улучшило Recall на 12%

---

## 🔬 Методология

### 1. Exploratory Data Analysis (EDA)
- Анализ распределений признаков
- Выявление пропущенных значений и аномалий
- Корреляционный анализ
- Bivariate analysis (Churn vs Features)

### 2. Feature Engineering
- Создание `tenure_group` (группировка по сроку)
- `total_services` (количество подключенных услуг)
- `price_per_service` (стоимость за услугу)
- `has_internet`, `has_support` (бинарные флаги)

### 3. Data Preprocessing
- Очистка `TotalCharges` (конвертация в float)
- Binary Encoding для Yes/No колонок
- One-Hot Encoding для категориальных признаков
- StandardScaler для нормализации

### 4. Model Training
- Baseline: Logistic Regression
- Сравнение моделей: Random Forest, Gradient Boosting, XGBoost
- Балансировка классов: SMOTE
- Лучшая модель: **XGBoost с SMOTE**

### 5. Model Evaluation
- Confusion Matrix
- ROC & Precision-Recall Curves
- Feature Importance Analysis
- Cross-Validation

---

## 💡 Бизнес-рекомендации

1. **Удержание новых клиентов**: Фокус на клиентов с tenure < 6 месяцев
2. **Стимулирование долгосрочных контрактов**: Скидки для перехода с month-to-month
3. **Улучшение Fiber Optic сервиса**: Выяснить причины недовольства
4. **Альтернативы Electronic Check**: Предложить автоматические списания
5. **Пакеты услуг**: Клиенты с большим количеством услуг реже уходят

---

## 🛠️ Технологический стек

- **Python 3.8+**
- **Data Science**: pandas, numpy, matplotlib, seaborn, plotly
- **Machine Learning**: scikit-learn, XGBoost, imbalanced-learn
- **Explainability**: SHAP
- **Notebooks**: Jupyter

---

## 📈 Roadmap

- [ ] Добавить SHAP analysis для интерпретируемости
- [ ] Создать веб-интерфейс (Streamlit/FastAPI)
- [ ] Dockerize приложение
- [ ] CI/CD pipeline
- [ ] Мониторинг модели в продакшене

---

## 👤 Автор

**Ваше Имя**

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 📄 Лицензия

Этот проект использует лицензию MIT. Подробности в файле [LICENSE](LICENSE).

---

## 🙏 Acknowledgments

- Датасет предоставлен IBM и доступен на [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- Вдохновлено лучшими практиками Data Science сообщества

---

⭐ **Если проект был полезен, поставьте звезду!** ⭐

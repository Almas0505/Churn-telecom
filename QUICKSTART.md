# 🚀 Руководство по быстрому старту

## Для разработчиков

### Шаг 1: Клонирование репозитория
```bash
git clone https://github.com/Almas0505/Churn-telecom.git
cd Churn-telecom
```

### Шаг 2: Установка зависимостей

#### Вариант A: Используя Makefile (рекомендуется)
```bash
make install
```

#### Вариант B: Используя pip напрямую
```bash
pip install -r requirements.txt
```

#### Вариант C: Для разработки (с dev зависимостями)
```bash
make install-dev
```

### Шаг 3: Загрузка данных
Скачайте датасет с [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) и поместите `WA_Fn-UseC_-Telco-Customer-Churn.csv` в `data/raw/`.

### Шаг 4: Обучение модели
```bash
# Вариант A: Через Makefile
make train

# Вариант B: Напрямую
cd src
python train.py
```

### Шаг 5: Оценка модели
```bash
# Вариант A: Через Makefile
make evaluate

# Вариант B: Напрямую
cd src
python evaluate.py
```

---

## Запуск веб-интерфейсов

### 🎨 Streamlit UI (интерактивная демонстрация)
```bash
streamlit run app.py
```
Откройте браузер: http://localhost:8501

### 🚀 FastAPI (REST API)
```bash
cd src
uvicorn api:app --reload
```
Откройте Swagger UI: http://localhost:8000/docs

---

## Использование Docker

### Вариант 1: Docker Compose (рекомендуется)

#### Обучение модели:
```bash
docker-compose up train
```

#### Запуск API:
```bash
docker-compose up api
```
API будет доступен на http://localhost:8000

#### Запуск Streamlit UI:
```bash
docker-compose up streamlit
```
UI будет доступен на http://localhost:8501

### Вариант 2: Docker напрямую

#### Сборка образа:
```bash
make docker-build
# или
docker build -t churn-prediction:latest .
```

#### Запуск:
```bash
docker run -v $(pwd)/data:/app/data -v $(pwd)/models:/app/models churn-prediction:latest
```

---

## Тестирование

### Запуск всех тестов:
```bash
make test
# или
pytest tests/ -v
```

### Запуск с coverage:
```bash
make test-cov
# или
pytest tests/ -v --cov=src --cov-report=html
```

Отчет coverage будет доступен в `htmlcov/index.html`

### Запуск конкретного теста:
```bash
pytest tests/test_features.py::test_create_total_services -v
```

---

## Проверка качества кода

### Линтинг:
```bash
make lint
```
Проверяет код с помощью flake8, black и mypy

### Форматирование:
```bash
make format
```
Автоматически форматирует код с помощью black

### Pre-commit hooks (рекомендуется):
```bash
pip install pre-commit
pre-commit install
```
Теперь при каждом commit автоматически запустятся проверки

---

## API Endpoints

После запуска FastAPI сервиса доступны следующие endpoints:

### GET `/` - Информация об API
```bash
curl http://localhost:8000/
```

### GET `/health` - Health check
```bash
curl http://localhost:8000/health
```

### POST `/predict` - Предсказание для одного клиента
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "tenure": 24,
    "MonthlyCharges": 70.5,
    "TotalCharges": 1692.0,
    "SeniorCitizen": 0,
    "Partner": 1,
    "Dependents": 0,
    "PhoneService": 1,
    "PaperlessBilling": 1
  }'
```

### GET `/docs` - Swagger UI
Откройте http://localhost:8000/docs в браузере

---

## Примеры использования Python API

### Обучение модели программно:
```python
from src.data_preparation import prepare_data
from src.features import engineer_features, encode_binary_features, encode_categorical_features
from src.train import split_data, scale_features, balance_data, train_model, save_artifacts

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
```

### Использование для предсказаний:
```python
from src.inference import ChurnPredictor
import pandas as pd

# Инициализация
predictor = ChurnPredictor(model_dir='models')
predictor.load_artifacts()

# Подготовка данных
customer_data = pd.DataFrame({
    'tenure': [24],
    'MonthlyCharges': [70.5],
    # ... остальные признаки
})

# Предсказание
results = predictor.predict_with_details(customer_data)
print(results)
```

### Валидация данных:
```python
from src.data_validation import DataValidator
import pandas as pd

# Инициализация валидатора
validator = DataValidator()

# Валидация
df = pd.read_csv('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')
is_valid = validator.validate(df)

# Отчет
validator.print_validation_report()
```

---

## Конфигурация

Все параметры проекта находятся в `config/config.yaml`:

```yaml
# Пример использования
from src.config import get_config

config = get_config()

# Доступ к параметрам
test_size = config.get('data.test_size')
model_type = config.get('model.type')
xgb_params = config.get('model.params.xgboost')
```

Вы можете редактировать `config/config.yaml` для изменения:
- Путей к данным
- Гиперпараметров модели
- Настроек препроцессинга
- Параметров логирования

---

## Логирование

Логи автоматически создаются в директории `logs/`:

```python
from src.logger import get_logger

logger = get_logger(__name__)

logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
```

---

## Структура проекта

```
Churn-telecom/
├── .github/workflows/     # CI/CD
├── config/                # Конфигурация
├── data/                  # Данные
├── models/                # Обученные модели
├── notebooks/             # Jupyter notebooks
├── reports/               # Отчеты и визуализации
├── src/                   # Исходный код
├── tests/                 # Тесты
├── app.py                 # Streamlit UI
├── Dockerfile             # Docker образ
├── docker-compose.yml     # Docker оркестрация
├── Makefile              # Автоматизация
├── requirements.txt       # Зависимости
└── setup.py              # Package setup
```

---

## Troubleshooting

### Проблема: "No module named 'src'"
**Решение:**
```bash
# Установите пакет в режиме разработки
pip install -e .
```

### Проблема: "Model not found"
**Решение:**
```bash
# Сначала обучите модель
python src/train.py
```

### Проблема: "Data file not found"
**Решение:**
Скачайте датасет с Kaggle и поместите в `data/raw/`

### Проблема: Docker container не стартует
**Решение:**
```bash
# Проверьте логи
docker-compose logs

# Пересоберите образ
docker-compose build --no-cache
```

---

## Дополнительные ресурсы

- 📖 [Полная документация](README.md)
- 📊 [Анализ проекта](PROJECT_ANALYSIS.md)
- 🎯 [Резюме улучшений](IMPROVEMENTS_SUMMARY.md)
- 🤝 [Руководство для контрибьюторов](CONTRIBUTING.md)

---

## Поддержка

Если возникли вопросы или проблемы:
1. Проверьте существующие Issues на GitHub
2. Создайте новый Issue с детальным описанием
3. Обратитесь к документации в README.md

---

**Готово к работе! 🎉**

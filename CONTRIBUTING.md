# Contributing to Churn Prediction Project

Спасибо за интерес к улучшению этого проекта! 🎉

## 📋 Как внести вклад

### 1. Reporting Issues

Если вы нашли баг или хотите предложить улучшение:

1. Проверьте, что issue еще не создан
2. Создайте новый issue с детальным описанием
3. Добавьте label (bug, enhancement, question)

### 2. Submitting Code

#### Шаги для создания Pull Request:

1. **Fork репозиторий**
   ```bash
   # Клонируйте свой fork
   git clone https://github.com/YOUR_USERNAME/Churn-telecom.git
   cd Churn-telecom
   ```

2. **Создайте ветку для изменений**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Установите зависимости для разработки**
   ```bash
   make install-dev
   # или
   pip install -r requirements.txt
   pip install pytest pytest-cov flake8 black mypy
   ```

4. **Внесите изменения**
   - Пишите чистый, читаемый код
   - Следуйте PEP 8 style guide
   - Добавьте docstrings для функций и классов
   - Пишите unit tests для нового функционала

5. **Запустите тесты и линтеры**
   ```bash
   make test          # Запустить тесты
   make lint          # Проверить код
   make format        # Форматировать код
   ```

6. **Commit и Push**
   ```bash
   git add .
   git commit -m "feat: Add feature description"
   git push origin feature/your-feature-name
   ```

7. **Создайте Pull Request**
   - Перейдите на GitHub
   - Создайте PR из вашей ветки в main
   - Детально опишите изменения

## 🎨 Code Style

### Python Style Guide

- Следуйте [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Максимальная длина строки: 127 символов
- Используйте `black` для форматирования
- Добавляйте type hints где возможно

### Docstrings

Используйте Google style docstrings:

```python
def function_name(param1: int, param2: str) -> bool:
    """
    Short description of function
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is negative
    """
    pass
```

### Commit Messages

Следуйте [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - новая функциональность
- `fix:` - исправление бага
- `docs:` - изменения в документации
- `style:` - форматирование кода
- `refactor:` - рефакторинг кода
- `test:` - добавление тестов
- `chore:` - обновление зависимостей, конфигурации

Примеры:
```
feat: Add SHAP explainability module
fix: Handle missing values in TotalCharges
docs: Update README with Docker instructions
test: Add tests for feature engineering
```

## 🧪 Testing

### Writing Tests

- Все новые функции должны иметь tests
- Тесты должны быть в директории `tests/`
- Используйте pytest
- Стремитесь к coverage > 80%

Пример теста:
```python
def test_function_name():
    """Test that function works correctly"""
    # Arrange
    input_data = ...
    
    # Act
    result = function_name(input_data)
    
    # Assert
    assert result == expected_value
```

### Running Tests

```bash
# Все тесты
make test

# С coverage
make test-cov

# Конкретный файл
pytest tests/test_features.py -v

# Конкретный тест
pytest tests/test_features.py::test_create_total_services -v
```

## 📁 Project Structure

```
Churn-telecom/
├── src/                    # Source code
│   ├── data_preparation.py
│   ├── features.py
│   ├── train.py
│   ├── evaluate.py
│   ├── inference.py
│   ├── data_validation.py
│   ├── config.py
│   └── logger.py
├── tests/                  # Unit tests
│   ├── test_data_preparation.py
│   ├── test_features.py
│   └── ...
├── config/                 # Configuration files
├── data/                   # Data files
├── models/                 # Trained models
├── reports/                # Reports and figures
└── notebooks/              # Jupyter notebooks
```

## 🔍 Code Review Process

После создания PR:

1. CI/CD автоматически запустит тесты и линтеры
2. Maintainer проведет code review
3. Внесите исправления если требуется
4. После одобрения PR будет смерджен

## 🐛 Reporting Bugs

При создании bug report включите:

- Версию Python
- Версии зависимостей
- Шаги для воспроизведения
- Ожидаемое и фактическое поведение
- Error traceback если есть

## 💡 Suggesting Enhancements

При предложении улучшений опишите:

- Зачем это нужно
- Как это должно работать
- Примеры использования
- Возможные альтернативы

## 📝 Documentation

- Обновляйте README.md при необходимости
- Добавляйте docstrings для нового кода
- Создавайте примеры использования
- Обновляйте CHANGELOG.md

## ⚖️ License

Внося вклад в проект, вы соглашаетесь, что ваш код будет лицензирован под MIT License.

## ❓ Questions?

Если есть вопросы:

- Создайте issue с label "question"
- Напишите в Discussions (если включены)

---

**Спасибо за вклад в проект! 🚀**

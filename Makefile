.PHONY: help install install-dev clean lint format test test-cov train evaluate docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install      - Install project dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make clean        - Remove build artifacts and caches"
	@echo "  make lint         - Run code quality checks"
	@echo "  make format       - Format code with black"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make train        - Train the model"
	@echo "  make evaluate     - Evaluate the model"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov flake8 black mypy pre-commit

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ htmlcov/ .coverage coverage.xml

lint:
	@echo "Running flake8..."
	flake8 src tests --max-line-length=127 --extend-ignore=E203,W503 || true
	@echo "\nRunning black check..."
	black --check src tests || true
	@echo "\nRunning mypy..."
	mypy src --ignore-missing-imports || true

format:
	black src tests

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

train:
	cd src && python train.py

evaluate:
	cd src && python evaluate.py

docker-build:
	docker build -t churn-prediction:latest .

docker-run:
	docker run -v $(PWD)/data:/app/data -v $(PWD)/models:/app/models churn-prediction:latest

# Setup pre-commit hooks
setup-hooks:
	pre-commit install

# Run all checks before committing
pre-commit: format lint test
	@echo "All checks passed! Ready to commit."

# Makefile
.PHONY: install dev test lint format run docker-up docker-down migrate clean

install:
	pip install -e ".[dev]"

dev:
	uvicorn src.resume_matcher.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v --cov=src/resume_matcher

lint:
	ruff check src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff check --fix src/ tests/

run:
	uvicorn src.resume_matcher.main:app --host 0.0.0.0 --port 8000

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

migrate:
	alembic upgrade head

migrate-create:
	alembic revision --autogenerate -m "$(msg)"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov/ dist/ build/ *.egg-info
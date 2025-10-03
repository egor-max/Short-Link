MSG = ""

.PHONY:
	downgrade
	clean
	install
	migrate
	makemigration
	run


clean:
	find . -name "*.pyc" -delete
	find . -name "*.log" -delete
	find . -name "*.log.*" -delete
	find . -name "__pycache__" -type d -exec rm -r {} +
	find . -name ".ruff_cache" -type d -exec rm -r {} +
	find .. -name ".ruff_cache" -type d -exec rm -r {} +
	find .. -name ".mypy_cache" -type d -exec rm -r {} +

migrate:
	uv run alembic upgrade head

downgrade:
	uv run alembic downgrade -1

makemigration:
	uv run alembic revision --autogenerate -m "$(MSG)"

run:
	uv run uvicorn app.main:app --reload

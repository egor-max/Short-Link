Инициализировать Alembic в проекте (должен использоваться асинхронный шаблон)
uv run alembic init --template async alembic 


При первом запуске указать нулевое состояние базы
uv run alembic stamp head


Создать миграции, если внесены изменения в `/orm`
uv run alembic revision --autogenerate -m "Your commit"
 

Применить миграции
uv run alembic upgrade head
#!/bin/bash

# Ожидание базы данных, если используется Postgres
# while ! nc -z "$DB_HOST" "$DB_PORT"; do
#   echo "Waiting for database at $DB_HOST:$DB_PORT..."
#   sleep 0.5
# done

# Если используешь Alembic и Postgres, раскомментируй:
# alembic upgrade head

# Запуск приложения Litestar
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

Отчет по выполнению лабораторных работ (№1–5)
Проект представляет собой асинхронный REST API сервис на Python 3.11 + Litestar + SQLAlchemy 2.0. Реализована архитектура N-уровней (Controller → Service → Repository) с подключением к PostgreSQL. Настроена полная контейнеризация и система контроля качества кода.

Реализованный функционал (ЛР 1–5)
1. Архитектура и БД

Спроектирована ORM-модель User с полями id, name, email.

Настроено асинхронное подключение к PostgreSQL через asyncpg

Реализован паттерн Repository для работы с данными

Реализован паттерн Service для бизнес-логики

Внедрение зависимостей (DI) через Litestar

API эндпоинт: GET /users с пагинацией (count, page)

2. Контейнеризация (Лабораторная №5)

Dockerfile для сборки образа приложения

entrypoint.sh с автоматическими миграциями БД

docker-compose.yml для оркестрации: App + PostgreSQL + pgAdmin

Pre-commit хуки: black, isort, pylint

100 тестовых пользователей с реалистичными данными

3. Качество кода

Автоматическое форматирование (black, isort)

Статический анализ (pylint)

Проверки запускаются при каждом git commit

Запуск проекта через Docker
1. Подготовка

bash
chmod +x entrypoint.sh
2. Сборка и запуск

bash
docker compose up -d
3. Доступ к сервисам

Сервис	URL	Описание
API	http://localhost:8000/users	Список пользователей (100 записей)
Swagger	http://localhost:8000/docs	Полная документация API
pgAdmin	http://localhost:5050	Интерфейс БД
PostgreSQL	localhost:5432	postgres / test_db
pgAdmin: admin@example.com / admin

4. Остановка

bash
docker compose down
Наполнение тестовой БД (100 пользователей)
bash
docker compose exec db psql -U postgres -d test_db -c "
INSERT INTO users (name, email) 
SELECT 
  CASE 
    WHEN id % 10 = 1 THEN 'John Smith'
    WHEN id % 10 = 2 THEN 'Sarah Johnson'
    WHEN id % 10 = 3 THEN 'Mike Brown'
    WHEN id % 10 = 4 THEN 'Emily Davis'
    WHEN id % 10 = 5 THEN 'David Wilson'
    WHEN id % 10 = 6 THEN 'Lisa Anderson'
    WHEN id % 10 = 7 THEN 'James Taylor'
    WHEN id % 10 = 8 THEN 'Anna Martinez'
    WHEN id % 10 = 9 THEN 'Robert Thomas'
    ELSE 'Jennifer Lee'
  END,
  LOWER(SPLIT_PART(name, ' ', 1) || SPLIT_PART(name, ' ', 2) || id || '@company.com')
FROM generate_series(1, 100);
"
Проверка качества кода
bash
# Все проверки разом
pre-commit run --all-files

# Только форматирование
black . && isort .

# Только линтинг
pylint app/
Тестирование API
bash
# Все пользователи
curl http://localhost:8000/users

# Пагинация (страница 2, по 5 записей)
curl "http://localhost:8000/users?count=5&page=2"

# JSON ответ:
# {
#   "items": [{"id": 11, "name": "John Smith", "email": "johnsmith11@company.com"}],
#   "total": 100
# }

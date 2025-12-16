FROM python:3.11-slim
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем Python пакеты
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВСЕ файлы app/ в /app (корень!)
COPY app/ .

EXPOSE 8000

# Ждём БД и запускаем
CMD sh -c "
  echo '⏳ Waiting for PostgreSQL...';
  for i in {1..30}; do
    if nc -z db 5432; then
      echo 'PostgreSQL ready!';
      break;
    fi;
    sleep 1;
  done;
  echo 'Starting Uvicorn...';
  exec python -m uvicorn main:app --host 0.0.0.0 --port 8000
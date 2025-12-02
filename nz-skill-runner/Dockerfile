# nz-skill-runner Dockerfile (Каноническая Версия v76.0)
# Этот файл описывает, КАК собрать образ нашего сервиса.
FROM python:3.11-slim

# Метаданные образа для лучшей идентификации и управления
LABEL maintainer="Nick Zhukoff <3327263@gmail.com>"
LABEL org.opencontainers.image.title="nz-skill-runner"
LABEL org.opencontainers.image.description="Skill Runner for the Genesis Project (nz- prefix)"
LABEL org.opencontainers.image.source="https://gitea.nzs.pp.ua/dbzhukoff/genesis-images"

WORKDIR /app

# Устанавливаем минимальные системные зависимости и очищаем кэш для уменьшения размера образа.
# ca-certificates необходим для надежной работы HTTPS (git, curl).
RUN apt-get update \
 && apt-get install -y --no-install-recommends git curl ca-certificates \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Устанавливаем Python-зависимости, не сохраняя кэш
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код нашего приложения
COPY src/ ./src/

# Указываем, что контейнер будет слушать на порту 8000
EXPOSE 8000

# Healthcheck для автоматической проверки состояния контейнера Докером
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD curl -f http://127.0.0.1:8000/health || exit 1

# Команда для запуска сервиса
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
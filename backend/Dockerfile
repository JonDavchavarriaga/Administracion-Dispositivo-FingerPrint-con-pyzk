FROM python:3.11-slim

# Evita archivos .pyc y buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código
COPY . .

# Puerto de FastAPI
EXPOSE 8000

# Comando CORRECTO para levantar FastAPI
CMD ["sh", "-c", "if [ \"$MOCK_MODE\" = \"True\" ] || [ \"$MOCK_MODE\" = \"true\" ]; then uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}; else alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}; fi"]

FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --system --create-home --uid 1001 appuser && \
    chown -R appuser:appuser /app

USER 1001

EXPOSE 8080

CMD ["python", "-m", "flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "8080"]

FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install --upgrade pip && pip install uv && uv sync

COPY main.py db.json ./
COPY templates templates

EXPOSE 5000

CMD ["uv", "run", "main.py"]

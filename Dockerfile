FROM python:3.11-slim

WORKDIR /app

COPY src/pyproject.toml src/uv.lock ./
RUN pip install --upgrade pip && pip install uv && uv sync

COPY src .

EXPOSE 5000

CMD ["uv", "run", "app.py"]

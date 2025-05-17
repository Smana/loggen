# syntax=docker/dockerfile:1

# ---- Base image ----
FROM python:3.13-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Development image ----
FROM base AS development
RUN pip install --upgrade pip && pip install uv
COPY . .
RUN uv venv
RUN . .venv/bin/activate && uv pip install --editable .
RUN . .venv/bin/activate && uv pip install -r pyproject.toml
USER 10001:10001
CMD [".venv/bin/python", "-m", "loggen"]

# ---- Production image ----
FROM base AS production
RUN pip install --upgrade pip && pip install uv
COPY loggen/ ./loggen/
COPY pyproject.toml LICENSE ./
RUN uv pip install --system .
USER 10001:10001
ENTRYPOINT ["python", "-m", "loggen"]

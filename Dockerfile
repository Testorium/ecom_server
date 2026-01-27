FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY ./pyproject.toml .
COPY ./uv.lock .

RUN uv sync --frozen --no-cache

COPY ./app .
COPY ./migrations ./migrations

RUN chmod +x ./prestart.sh
RUN chmod +x ./run

ENTRYPOINT ["./prestart.sh"]
CMD ["./run"]
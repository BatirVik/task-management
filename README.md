# Task Management REST API | Test Assignment

> https://www.loom.com/share/feb08958d1ff48e18135fb92a5c842c0?sid=8fe9b5d8-746c-4cce-a65c-94c2425804f8

## Requirements

-  [uv](https://docs.astral.sh/uv/)
-  [docker](https://www.docker.com/)

## Run

Create a file `.env` at the root of the project and populate it with the required environment variables. After that, execute:

```bash
uv run main.py
```

## Environment Variables

-  DB_URL
-  PORT (optional)
-  HOST (optional)

## Test

Run the PostgreSQL container:
```bash
docker run -d \
  --name test-pg \
  -e POSTGRES_USER=test \
  -e POSTGRES_PASSWORD=test \
  -e POSTGRES_DATABASE=test \
  -p 5433:5432 \
  postgres:latest
```

Create a file `.env.test` at the root of the project with the content below:
```env
DB_URL="postgresql+psycopg://test:test@localhost:5433/test"
```

Run tests:
```bash
uv run pytest
```

## Migrations
Create a migration file:
```bash
uv run alembic revision --autogenerate -m "message"
```
Apply the latest migrations:
```bash
uv run alembic upgrade head
```

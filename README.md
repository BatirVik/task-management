# Task Managment REST API | Test Assingment

## Requirments

- [uv](https://docs.astral.sh/uv/)
- [docker](https://www.docker.com/)

## Run

Create a file `.env` at the root of the project and populate it with the required environment variables. After that, execute:

```bash
uv run main.py
```

## Environment Variables

- DB_URL
- PORT (optional)
- HOST (optional)

## Test

Run PostgreSQL container:
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
DB_URL="postgresql+psycopg://test:test@localhost:5433/test
```

Run tests:
```bash
uv run pytest
```

## Migrations
Create a migration file:
```bash
alembic revision --autogenerate -m "message"
```
Apply the latest migrations:
```bash
alembic upgrade head
```





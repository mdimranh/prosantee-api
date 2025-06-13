# FastAPI Application with SQLModel

A modern FastAPI application implementing best practices with SQLModel, Alembic migrations, and DRF-like generic views.

## Features

- FastAPI for high-performance API development
- SQLModel for type-safe database operations
- Alembic for database migrations
- Generic CRUD operations
- Async database operations with PostgreSQL
- Environment-based configuration
- Structured project layout

## Project Structure

```
.
├── api/
│   └── v1/
│       ├── [app_name]/
│       │   ├── service.py
│       │   ├── route.py
│       └── router.py
├── db/
│   ├── migrations/
│   │   └── env.py
│   ├── base.py
│   ├── config.py
│   └── database.py
├── models/
│   └── [app_name].py
├── .env.example
├── alembic.ini
├── app.py
└── requirements.txt
```

## Setup

1. Clone the repository

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
cp .env.example .env
```
Edit the .env file with your database credentials and other configurations.

5. Initialize the database:
```bash
py -m alembic upgrade head
```

6. Run the application:
```bash
uvicorn app:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Migrations

To create a new migration:
```bash
py -m alembic revision --autogenerate -m "description of changes"
```

To apply migrations:
```bash
py -m alembic upgrade head
```

## Development

### Adding New Models

1. Create a new model in `db/models/`
2. Import the model in `db/models/__init__.py`
3. Create migrations using Alembic
4. Create corresponding API endpoints in `api/v1/endpoints/`
5. Register the new router in `api/v1/router.py`

### Best Practices

- Use type hints everywhere
- Follow FastAPI's dependency injection patterns
- Keep the single responsibility principle
- Write tests for new features
- Document your API endpoints
- Use async/await consistently

## License

MIT
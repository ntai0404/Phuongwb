# Core API Service

Central backend service for Phuong Web application.

## Features

- **Authentication & Authorization**: JWT-based auth with RBAC (User/Admin roles)
- **RSS Source Management**: CRUD operations for RSS feed sources
- **Article Management**: View and manage crawled articles
- **Crawler Orchestration**: Trigger and schedule crawl tasks
- **Background Worker**: Processes crawled articles from RabbitMQ

## Technology Stack

- FastAPI
- SQLAlchemy (PostgreSQL ORM)
- Pydantic (Data validation)
- python-jose (JWT tokens)
- passlib (Password hashing)
- pika (RabbitMQ client)

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/users/me` - Get current user
- `GET /api/v1/auth/users` - List users (Admin)
- `PUT /api/v1/auth/users/{id}/role` - Update user role (Admin)

### RSS Sources
- `GET /api/v1/sources` - List RSS sources
- `POST /api/v1/sources` - Add RSS source (Admin)
- `PUT /api/v1/sources/{id}` - Update RSS source (Admin)
- `DELETE /api/v1/sources/{id}` - Delete RSS source (Admin)

### Articles
- `GET /api/v1/articles` - List articles (with filters)
- `GET /api/v1/articles/{id}` - Get article details
- `DELETE /api/v1/articles/{id}` - Delete article (Admin)

### Crawler Orchestration
- `POST /api/v1/crawler/trigger` - Trigger immediate crawl (Admin)
- `PUT /api/v1/crawler/schedule` - Update crawl schedule (Admin)
- `GET /api/v1/crawler/schedule` - Get crawl schedule (Admin)

## Environment Variables

- `DB_HOST` - PostgreSQL host (default: postgres)
- `DB_PORT` - PostgreSQL port (default: 5432)
- `DB_NAME` - Database name (default: newsdb)
- `DB_USER` - Database user (default: postgres)
- `DB_PASSWORD` - Database password (default: postgres)
- `RABBITMQ_HOST` - RabbitMQ host (default: rabbitmq)
- `RABBITMQ_PORT` - RabbitMQ port (default: 5672)
- `RABBITMQ_USER` - RabbitMQ user (default: guest)
- `RABBITMQ_PASSWORD` - RabbitMQ password (default: guest)
- `RECOMMENDATION_URL` - Recommendation service URL
- `SECRET_KEY` - JWT secret key

## Running

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn src.main:app --host 0.0.0.0 --port 8080
```

## Docker

```bash
docker build -t core-api-service .
docker run -p 8080:8080 core-api-service
```

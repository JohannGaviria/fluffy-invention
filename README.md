# fluffy-invention

**Fluffy Invention** is a medical appointment management system designed to bring order to the everyday chaos of a healthcare institution. Its purpose is simple: ensure that every medical appointment — **from the patient’s request to the physician’s consultation** — flows smoothly, without friction or loss of context.

The project takes processes that are often fragmented across phone calls, paper forms, and legacy systems, and centralizes them into a single, clear, fast, and reliable platform.

**Fluffy Invention** manages the complete appointment lifecycle: user registration, medical availability lookup, appointment creation and modification, automated notifications, on-site check-in, and consultation record tracking. All of this happens within a unified environment designed around real actors and workflows: patients clearly understand when and with whom they will be seen, physicians focus only on relevant appointments, and front-desk staff maintain control of daily operations without overload.

Rather than aiming to be a massive all-in-one solution, **Fluffy Invention** serves as a solid foundation for building a scalable clinical services ecosystem. The system is built on modern technologies that prioritize performance, asynchronicity, and long-term scalability without unnecessary complexity.

## Technologies

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/doc/)[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)[![REST API](https://img.shields.io/badge/REST_API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://restfulapi.net/)[![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/)[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/docs/)[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/docs/)[![SQLModel](https://img.shields.io/badge/SQLModel-1C3C3C?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlmodel.tiangolo.com/)[![Alembic](https://img.shields.io/badge/Alembic-3D3D3D?style=for-the-badge&logo=alembic&logoColor=white)](https://alembic.sqlalchemy.org/)[![PyJWT](https://img.shields.io/badge/PyJWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://pyjwt.readthedocs.io/)[![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)[![Pub/Sub](https://img.shields.io/badge/Pub%2FSub-000000?style=for-the-badge&logo=rabbitmq&logoColor=white)](https://cloud.google.com/pubsub/docs)[![Ruff](https://img.shields.io/badge/Ruff-000000?style=for-the-badge&logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)[![mypy](https://img.shields.io/badge/mypy-233564?style=for-the-badge&logo=mypy&logoColor=white)](https://mypy.readthedocs.io/)[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/)[![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://swagger.io/docs/)[![Logs](https://img.shields.io/badge/Logs-000000?style=for-the-badge&logo=logstash&logoColor=white)](https://www.elastic.co/guide/en/logstash/current/index.html)[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://docs.github.com/actions)[![CI/CD](https://img.shields.io/badge/CI%2FCD-000000?style=for-the-badge&logo=github&logoColor=white)](https://about.gitlab.com/topics/ci-cd/)[![PyTest](https://img.shields.io/badge/PyTest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)[![Monolith](https://img.shields.io/badge/Monolith-6C63FF?style=for-the-badge)](https://en.wikipedia.org/wiki/Monolithic_application)[![Event-Driven](https://img.shields.io/badge/Event-Driven-E91E63?style=for-the-badge)](https://en.wikipedia.org/wiki/Event-driven_architecture)[![Clean Architecture](https://img.shields.io/badge/Clean_Architecture-00A86B?style=for-the-badge)](https://en.wikipedia.org/wiki/Clean_architecture)[![Hexagonal Architecture](https://img.shields.io/badge/Hexagonal-FFB300?style=for-the-badge)](https://en.wikipedia.org/wiki/Hexagonal_architecture)

---

## Quickstart

### Clone the repository

```bash
git clone git@github.com:JohannGaviria/fluffy-invention.git
cd fluffy-invention
```

### Copy environment variables

Copy `.env.example` to `.env` and edit as needed, or set the variables directly in your environment. See the table below for required variables.

```bash
cp .env.example .env
```

| Category               | Key               | Description                                                              | Example                                                                              |
| -----------------------| ------------------| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------|
| Application Metadata   | APP_NAME          | Human-readable name of the application                                   | Fluffy Invention                                                                     |
| Application Metadata   | APP_SUMMARY       | Short summary describing the main purpose of the application             | System to manage medical appointments efficiently and centrally                      |
| Application Metadata   | APP_DESCRIPTION   | Detailed description of the application and its business context         | Medical appointment management system for healthcare institutions                    |
| Backend Configuration  | DEBUG             | Enables or disables debug mode for development and troubleshooting       | True                                                                                 |
| Backend Configuration  | ENVIRONMENT       | Defines the runtime environment where the application is running         | development                                                                          |
| Backend Configuration  | BACKEND_PORT      | Network port where the backend service listens for incoming requests     | 8000                                                                                 |
| Backend Configuration  | BACKEND_WORKERS   | Number of worker processes used by the backend server to handle requests | 4                                                                                    |
| Backend Configuration  | LOG_LEVEL         | Logging verbosity level used by the application                          | INFO                                                                                 |
| Database Configuration | DATABASE_URL      | Full database connection string                                          | postgresql+psycopg2://postgres:password@fluffy-invention-db:5432/fluffy_invention_db |
| Database Configuration | DB_PORT           | Port where the database service is exposed                               | 5432                                                                                 |
| Database Configuration | POSTGRES_USER     | Username used to authenticate with the PostgreSQL database               | fluffy_user                                                                          |
| Database Configuration | POSTGRES_PASSWORD | Password used to authenticate with the PostgreSQL database               | supersecret                                                                          |
| Database Configuration | POSTGRES_DB       | Name of the PostgreSQL database                                          | fluffy_db                                                                            |
| Redis Configuration    | REDIS_HOST        | Hostname or service name of the Redis instance                           | redis                                                                                |
| Redis Configuration    | REDIS_PORT        | Port where the Redis service is exposed                                  | 6379                                                                                 |
| Redis Configuration    | REDIS_PASSWORD    | Password for authenticating with Redis (if enabled)                      | redispass                                                                            |
| Redis Configuration    | REDIS_DB          | Redis database index used by the application                             | 0                                                                                    |

---

### Run in a Docker environment

#### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

#### Running the Service with Docker

You can easily start the backend, database, and other services using Docker Compose:

```bash
docker compose up --build
```

Alternatively, if tou prefer using the Makefile:

```bash
make up
```

Once the services are running, the API will be accessible at:

[http://localhost:8000/docs](http://localhost:8000/docs) – this provides the **interactive Swagger UI** for testing all endpoints.

---

## License

Distributed under the **MIT License**. See [LICENSE](./LICENSE) for details.

---

> Made with ♥️ by [JohannGaviria](https://github.com/JohannGaviria) – always happy to connect for feedback, collaboration, or job opportunities.

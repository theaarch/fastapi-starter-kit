# FastAPI Starter Kit

A production-ready, highly modern starter kit for building scalable asynchronous APIs with FastAPI, SQLAlchemy 2.0, Pydantic v2, and PostgreSQL.

---

## Features

- **⚡ Modern Framework**: Built with **FastAPI** featuring asynchronous endpoints, modular routers, dependency injection with `Annotated`, and clean **Lifespan** context management for graceful resource shutdown.
- **🌐 Cross-Origin Resource Sharing**: Configurable **CORSMiddleware** with environment-controlled origins (`CORS_ORIGINS`).
- **🛠️ Package Management**: Blazing fast dependency resolution and virtual environments via **[uv](https://github.com/astral-sh/uv)**.
- **🗄️ Asynchronous Database & ORM**: **SQLAlchemy 2.0** (`Mapped`, `mapped_column`, `select()`) powered by **asyncpg** driver, connection pooling, and `server_default=func.now()` timestamps.
- **🔄 Database Migrations**: **Alembic** pre-configured for asynchronous execution, organized under `app/alembic/` with standardized constraint naming conventions.
- **🛡️ Secure Authentication**:
  - OWASP-recommended **Argon2id** password hashing via **pwdlib**.
  - Stateless **JWT** access tokens via **PyJWT** with explicit algorithm verification and strict expiration.
- **✨ Strict Type Precision**: Built for **Python >= 3.14** using PEP 604 union types (`|`), `Self`, and strict type annotations across routes and dependencies.
- **🔍 Validation & Settings**: **Pydantic v2** (`BaseModel`, `ConfigDict(from_attributes=True)`) and **pydantic-settings** with `.env` file management.
- **🧪 Testing & Tooling**:
  - Test suite with **pytest**, **pytest-asyncio** (auto mode), and **httpx** (`ASGITransport`).
  - Ultra-fast code linting, formatting, and helper scripts via **Ruff** and `scripts/lint.sh`.
  - **Docker Compose** configuration for instantaneous local PostgreSQL setup.

---

## Project Structure

```
fastapi-starter-kit/
├── app/
│   ├── alembic/                # Alembic database migrations & versions
│   │   ├── versions/           # Migration revision scripts
│   │   └── env.py              # Async migration engine runner
│   ├── api/                    # API route controllers & dependencies
│   │   ├── auth/               # Authentication endpoints (login, register, profile, etc.)
│   │   └── dependencies.py     # Shared route dependencies (get_current_user, etc.)
│   ├── core/                   # Application core configuration & services
│   │   ├── config.py           # Pydantic Settings & environment parsing
│   │   ├── database.py         # Async SQLAlchemy engine & session maker
│   │   └── security.py         # Argon2 hashing & JWT encoding/decoding
│   ├── models/                 # SQLAlchemy 2.0 ORM models
│   │   ├── base.py             # DeclarativeBase with constraint naming conventions
│   │   └── user.py             # User model with server-side timestamps
│   └── schemas/                # Pydantic v2 schemas for request & response validation
│       ├── common.py           # Generic response schemas
│       ├── token.py            # Token & payload schemas
│       └── user.py             # User request/response schemas
├── scripts/
│   └── lint.sh                 # Code checking & auto-formatting shell script
├── tests/                      # Unit & integration test suite
│   ├── api/                    # Route & API integration tests
│   └── core/                   # Core security & configuration tests
├── .github/
│   ├── dependabot.yml          # Automated dependency security updates
│   └── workflows/
│       └── ci.yml              # Automated GitHub Actions CI pipeline
├── alembic.ini                 # Alembic configuration file
├── docker-compose.yml          # Local PostgreSQL container service
├── Dockerfile                  # Multi-stage production container image definition
├── main.py                     # FastAPI application factory & root entrypoint
├── pyproject.toml              # Project dependencies, build system & tool configs
└── uv.lock                     # Deterministic dependency lockfile
```

---

## Prerequisites

- **Python**: `>= 3.14`
- **uv**: Modern Python package manager ([Installation Guide](https://github.com/astral-sh/uv))
- **Docker**: Optional, for running local PostgreSQL via Docker Compose

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/theaarch/fastapi-starter-kit.git
cd fastapi-starter-kit
```

### 2. Environment Configuration

Copy the example environment configuration file:

```bash
cp .env.example .env
```

Review and adjust `.env` parameters as needed:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `APP_NAME` | Name of the application | `"FastAPI Starter Kit"` |
| `APP_URL` | Base URL of the service | `http://localhost:8000` |
| `CORS_ORIGINS` | Allowed CORS origins (JSON array) | `'["*"]'` |
| `API_PREFIX` | Prefix for versioned endpoints | `"/api"` |
| `SECRET_KEY` | Secret key for JWT signing | *Secure random string* |
| `ALGORITHM` | JWT signing algorithm | `"HS256"` |
| `ACCESS_TOKEN_EXPIRATION` | Access token lifetime in minutes | `1440` (24 hours) |
| `DB_URL` | Async PostgreSQL connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db` |

### 3. Start Local Database (Optional via Docker)

Start a local PostgreSQL 16 instance with Docker Compose:

```bash
docker compose up -d
```

### 4. Install Dependencies

Install all runtime and development dependencies:

```bash
uv sync
```

### 5. Run Database Migrations

Apply existing Alembic database migrations:

```bash
uv run alembic upgrade head
```

To create a new migration after editing models in `app/models/`:

```bash
uv run alembic revision --autogenerate -m "create_example_table"
```

### 6. Start Development Server

Run the development server with hot-reload enabled:

```bash
uv run uvicorn main:app --reload
```

The server will be running at [http://localhost:8000](http://localhost:8000).

---

## Interactive API Documentation

Once the server is running, explore the interactive documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Schema**: [http://localhost:8000/api/openapi.json](http://localhost:8000/api/openapi.json)

---

## Available API Endpoints

All endpoints are grouped logically:

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/` | Service root welcome message | No |
| `GET` | `/health` | Cloud-native liveness and readiness probe | No |
| `POST` | `/api/auth/register` | Register a new user account | No |
| `POST` | `/api/auth/login` | Authenticate user and receive JWT token | No |
| `POST` | `/api/auth/logout` | Terminate session | Yes (`Bearer`) |
| `GET` | `/api/auth/me` | Retrieve profile of authenticated user | Yes (`Bearer`) |
| `PUT` | `/api/auth/me` | Update name or email address | Yes (`Bearer`) |
| `PUT` | `/api/auth/user/password` | Change password with current credential verification | Yes (`Bearer`) |

---

## Testing & Code Quality

### Running Tests

Execute all async tests with `pytest`:

```bash
uv run pytest
```

### Code Formatting & Linting

You can run checks using the included `scripts/lint.sh` helper script:

```bash
# Check code for lint errors and formatting
./scripts/lint.sh

# Automatically fix lint issues and format files
./scripts/lint.sh --fix
```

Alternatively, invoke `Ruff` directly:

```bash
# Check lint errors
uv run ruff check .

# Apply formatting
uv run ruff format .
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).

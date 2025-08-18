# Auth-service

Python code for authentication service

## Requirements

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) or Docker Engine (Linux).
* `.env` file with environment variables.
* Firebase credentials `./credentials/firebase_account.json`.

##  Project structure 📁

```bash
📁 AUTH-SERVICE/                      # Root directory of the authentication microservice
│
├── 📁 app/                       # Main application code
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point, configures routes and middleware
│   │
│   ├── 📁 core/                  # Core system configurations and functionalities
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration variables and environment settings
│   │   ├── firebase_config.py     # Firebase Authentication specific configuration
│   │   ├── security.py            # Security utilities (JWT, password hashing, etc.)
│   │   ├── exceptions.py          # Custom exceptions for authentication domain
│   │   └── logging.py             # Logging system configuration
│   │
│   ├── 📁 domain/                    # Domain layer - Pure business logic (Clean Architecture)
│   │   ├── __init__.py
│   │   ├── 📁 entities/              # Domain entities (business objects) - e.g. user.py
│   │   │   └──__init__.py
│   │   ├── 📁 repositories/          # Interfaces/contracts for data access - e.g. user_repository.py
│   │   │   └── __init__.py
│   │   └── 📁 services/              # Domain services with complex business logic - e.g. auth_service.py
│   │       └── __init__.py
│   │
│   ├── 📁 infrastructure/            # Infrastructure layer - Concrete technical implementations
│   │   ├── __init__.py
│   │   ├── 📁 database/              # Database configuration and models
│   │   │   ├── __init__.py
│   │   │   ├── mysql_connection.py # MySQL connection configuration
│   │   │   └── 📁 models/            # Database ORM models - e.g. user_model.py
│   │   │       └── __init__.py
│   │   ├── 📁 auth/                  # Specific authentication implementations
│   │   │   ├── __init__.py
│   │   │   ├── firebase_auth.py   # Concrete Firebase authentication implementation
│   │   │   └── token_validator.py # JWT/Firebase token validator
│   │   ├── 📁 repositories/          # Concrete repository implementations
│   │   │   ├── __init__.py
│   │   │   └── mysql_user_repository.py # MySQL repository implementation
│   │
│   ├── 📁 application/               # Application layer - Use cases and orchestration
│   │   ├── __init__.py
│   │   ├── 📁 use_cases/             # Application-specific use cases - e.g. login_user.py
│   │   │   └── __init__.py
│   │   ├── 📁 dto/                   # Data Transfer Objects - e.g. auth_dto.py
│   │   │   └── __init__.py
│   │   └── 📁 interfaces/            # Application layer interfaces - e.g. auth_service_interface.py
│   │       └── __init__.py
│   │
│   ├── 📁 presentation/              # Presentation layer - API and external interfaces
│   │   ├── __init__.py
│   │   ├── 📁 api/                   # REST API endpoints and configuration
│   │   │   ├── __init__.py
│   │   │   ├── 📁 v1/                # API version 1 endpoints
│   │   │   │   └── __init__.py
│   │   │   └── dependencies.py    # FastAPI shared dependencies (dependency injection)
│   │   ├── 📁 schemas/               # Pydantic schemas for validation and serialization - e.g. auth_schema.py
│   │   │   └── __init__.py
│   │   └── 📁 middleware/            # Custom application middleware
│   │       ├── __init__.py
│   │       ├── cors_middleware.py # CORS (Cross-Origin Resource Sharing) configuration
│   │       ├── logging_middleware.py # Request/response logging middleware
│   │       └── exception_handler.py # Global HTTP exception handlers
│   │
│   └── 📁 shared/                    # Shared utilities and constants across the application
│       ├── __init__.py
│       ├── constants.py           # Global application constants
│       ├── enums.py               # Enumerations (states, types, etc.)
│       └── utils.py               # General utility functions
│
├── 📁 tests/                        # Complete automated test suite
│   ├── __init__.py
│   ├── conftest.py               # Global pytest configuration (fixtures, setup)
│   ├── 📁 unit/                     # Unit tests - Test isolated components
│   │   ├── __init__.py
│   │   ├── domain/               # Domain layer tests - e.g. test_auth_service.py
│   │   ├── application/          # Application layer tests - e.g. test_use_cases.py
│   │   └── infrastructure/       # Infrastructure layer tests - e.g. test_repositories.py
│   ├── 📁 integration/              # Integration tests - e.g. test_api_endpoints.py
│   │   └── __init__.py
│   └── 📁 e2e/                      # End-to-end tests - e.g. test_auth_flow.py
│       └── __init__.py
│
├── 📁 scripts/                      # Automation scripts and utilities
│   ├── start.sh                  # Script to start the application in development
│   └── test.sh                   # Script to run the complete test suite
│
├── .env                          # Environment variables (should NOT be in git, use .env.example)
├── Dockerfile                    # Instructions to build Docker application image
├── docker-compose.yml            # Service orchestration (app, db, redis, etc.)
├── .gitignore                    # Files/directories ignored by Git
├── requirements.txt              # Python dependencies for pip
└── README.md                     # Main project documentation
```


## Steps to run the project

### Create .env file, for example:

```bash
AUTH_SERVICE_PORT=your_port
ENVIRONMENT=qa
MYSQL_HOST=your_host
MYSQL_PORT=your_db_port
MYSQL_USER=your_db_user
MYSQL_PASSWORD=your_db_password
MYSQL_DB=your_db
FIREBASE_API_KEY=your_firebase_api_key
```

### Load Firebase credentials .json in Root directory

```bash
📁 AUTH-SERVICE/
│
│
├── .gitignore
├── requirements.txt
└── firebase_account.json
```

### Run the service

```bash
docker compose up --build -d
```

### Check running containers in Docker Desktop / Docker Engine

```bash
docker ps
```

### Test the service

The service is running [Here](http://localhost:8000).


### Stop the service

```bash
docker compose down
```

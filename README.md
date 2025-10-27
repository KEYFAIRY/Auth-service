# Auth-service

Python code for authentication service

## Requirements

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) or Docker Engine (Linux).
* `.env` file with environment variables.
* Firebase credentials `./credentials/firebase_account.json`.

##  Project structure 📁

```bash
📁 AUTH-SERVICE/                  # Root directory of the authentication microservice
│
├── 📁 app/                       # Main application code
│   ├── main.py                    # FastAPI application entry point, configures routes and middleware
│   │
│   ├── 📁 core/                  # Core system configurations and functionalities
│   │   ├── config.py              # Configuration variables and environment settings
│   │   ├── firebase_config.py     # Firebase Authentication specific configuration
│   │   ├── exceptions.py          # Custom exceptions for authentication domain
│   │   └── logging.py             # Logging system configuration
│   │
│   ├── 📁 domain/                 # Domain layer - Pure business logic (Clean Architecture)
│   │   ├── 📁 entities/           # Domain entities (business objects) - e.g. user.py
│   │   ├── 📁 repositories/       # Interfaces/contracts for data access - e.g. user_repository.py
│   │   └── 📁 services/           # Domain services with complex business logic - e.g. auth_service.py
│   │
│   ├── 📁 infrastructure/         # Infrastructure layer - Concrete technical implementations
│   │   ├── 📁 database/           # Database configuration and models
│   │   │   └── 📁 models/         # Database ORM models - e.g. user_model.py
│   │   └── 📁 repositories/       # Concrete repository implementations
│   │
│   ├── 📁 application/            # Application layer - Use cases and orchestration
│   │   ├── 📁 use_cases/          # Application-specific use cases - e.g. login_user.py
│   │   └── 📁 dto/                # Data Transfer Objects - e.g. auth_dto.py
│   │
│   ├── 📁 presentation/           # Presentation layer - API and external interfaces
│   │   ├── 📁 api/                # REST API endpoints and configuration
│   │   │   ├── 📁 v1/             # API version 1 endpoints
│   │   │   └── dependencies.py    # FastAPI shared dependencies (dependency injection)
│   │   ├── 📁 schemas/            # Pydantic schemas for validation and serialization - e.g. auth_schema.py
│   │   └── 📁 middleware/         # Custom application middleware (exception handler, cors, logging)
│   │
│   └── 📁 shared/                 # Shared utilities (constants, enums, utils)
│
├── 📁 tests/                     # Complete automated test suite
│   ├── conftest.py               # Global pytest configuration (fixtures, setup)
│   ├── 📁 unit/                  # Unit tests - Test isolated components
│   │   ├── domain/               # Domain layer tests - e.g. test_auth_service.py
│   │   ├── application/          # Application layer tests - e.g. test_use_cases.py
│   │   └── infrastructure/       # Infrastructure layer tests - e.g. test_repositories.py
│
├── 📁 scripts/                   # Automation scripts (start application, runn tests)
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

Edit the .example.env file with actual variables, and rename it to .env

### Load Firebase credentials .json in Root directory

Load account service .json from firebase in root directory (AUTH-SERVICE/)

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

## Steps to run unit tests

### Create virtual environment:

```bash
python -m venv venv
```

### Activate virtual environment:

```bash
.\venv\Scripts\Activate.ps1
```

### Install pip:

```bash
python -m pip install --upgrade pip
```

### Install required test tools and project requirements:

```bash
pip install pytest pytest-asyncio pytest-cov
```

```bash
pip install -r requirements.txt
```

### Check installation:

```bash
pytest --version
```

### Execute test:

For example, for executing test in mysql_user_repository.py:
```bash
python -m pytest tests/auth_service.py -v --tb=short
```
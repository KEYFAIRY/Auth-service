# Auth-service

Python code for authentication service

## Requirements

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) or Docker Engine (Linux).
* `.env` file with environment variables.
* Firebase credentials `./credentials/firebase_account.json`.

##  Project structure

```bash
├── Auth-service/
│   └── 📁 Service/
│       ├── 📁 domain/                  # Pure business rules
│       │   ├── 📁 entities/            # Entities (User, Token)
│       │   ├── 📁 services/            # Use cases (create account, login)
│       ├── 📁 application/             # Orchestration logic and interfaces
│       │   ├── 📁 interfaces/          # Contracts for repositories and auth providers
│       │   ├── 📁 use_cases/            # Use case implementations
│       ├── 📁 infrastructure/          # Concrete adapters
│       │   ├── firebase_service.py   # Implements auth provider interface
│       │   ├── mysql_repository.py   # Implements repository interface
│       ├── 📁 presentation/             # Delivery layer
│       │   ├── 📁 routers/              # FastAPI endpoints
│       │   ├── 📁 schemas/              # Pydantic models
│       │   ├── dependencies.py
│       │   └── main.py
│       └── config.py
├── 📁 credentials/
│   └── firebase_account.json         # Firebase credentials (DO NOT COMMIT to Git)
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .gitignore
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

### Load Firebase credentials .json in credentials folder

```bash
📁 credentials/
│   └── firebase_account.json
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

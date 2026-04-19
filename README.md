# Online Store API

A training project for an online store with access rights, a shopping cart, and orders. Implemented using a modern asynchronous platform.

## Stack
- **Language:** Python 3.12.9 🐍
- **Framework:** FastAPI ⚡
- **ORM:** SQLAlchemy (Async) 🏗️
- **Database:** PostgreSQL 🐘
- **Cache:** Redis 🔴
- **Auth:** JWT (RS256) 🔐
- **Configuration:** Pydantic-Settings ✅
- **Deploy:** Docker 🐳

## Structure
```
.
├── src/                            # Source code of the application
│   ├── core/                       # Core logic (configs, database connection, global utilities)
|   |   ├── middlewares/            # Middlewares
|   ├── creds/                      # Authorization keys
│   └── modules/                    # Business logic divided by domain modules
│       ├── admin/                  # Administrative panel functionality
|       |   ├── orders/             # Orders control
|       |   ├── products/           # Products control
|       |   └── users/              # Users control
│       ├── card/                   # Shopping cart logic
│       ├── orders/                 # Order management system
│       ├── products/               # Product catalog and management
│       └── users/                  # User management and authentication
├── .env.example                    # Template for environment variables
├── Dockerfile                      # Docker image configuration
├── docker-compose.yml              # Docker Compose orchestration file
├── requirements.txt                # Requirements for project
└── README.md                       # Project documentation
```

# Installation

### Clone the repository
```bash
git clone https://github.com/DarkMonarch-DN/Online-Store.git
cd online_store
```

### Prepare encryption keys:
To use JWT (RS256), you need to create private and public keys in the src/creds/ folder
```bash
mkdir -p src/creds
openssl genrsa -out src/creds/jwt-private.pem 2048
openssl rsa -in src/creds/jwt-private.pem -outform PEM -pubout -out src/creds/jwt-public.pem
```

### Set up environment variables
```bash
cp .env.example .env
```

## 🚀 Quick Start (Docker)
Please note that this approach requires Docker to be installed. Also, be aware that Docker will download the PostgreSQL and Redis images when running.

### Running Docker Compose
```bash
docker compose up --build # -d Run in the background
```

## 💻 Local development (without Docker)
Please note that you must have postgresql and redis installed locally.

### Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run project
```bash
uvicorn "src.main:app" --reload --no-access-log
```

## 📖 Documentation
After launching the project, a detailed description of all endpoints is available in the Swagger UI: 
📌 http://localhost:8000/docs
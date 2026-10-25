# Kanban Board API (FastAPI)

A full-featured asynchronous Kanban Board web application and REST API built with FastAPI, SQLAlchemy 2.0 (async), PostgreSQL (asyncpg), Alembic, and JWT authentication.

## Features

- **Authentication & Authorization**: User registration and JWT-based login.
- **Board Management**: Create, view, update, and manage boards owned by authenticated users.
- **Columns & Cards**: Organize tasks across customizable workflow columns (To Do, In Progress, Done, etc.) with card ordering and descriptions.
- **Interactive UI**: Static frontend included for login and board view (`/static/login.html`, `/static/board.html`).
- **Database Migrations**: Managed via Alembic with async SQLAlchemy.
- **API Documentation**: Interactive Swagger UI (`/docs`) and ReDoc (`/redoc`).

## Tech Stack

- **Framework**: FastAPI
- **Database ORM**: SQLAlchemy (Async)
- **Database Driver**: `asyncpg` (PostgreSQL)
- **Migrations**: Alembic
- **Validation**: Pydantic v2 / Pydantic Settings
- **Auth**: Passlib (bcrypt) & Python-Jose / PyJWT

## Getting Started

### 1. Prerequisites
- Python 3.10+
- PostgreSQL database

### 2. Environment Setup
Clone the repository and create a virtual environment:

```bash
# Clone repository
git clone https://github.com/AdityaVarte/Kanban-fastAPI-.git
cd Kanban-fastAPI-

# Create and activate virtual environment
python -m venv venv
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the project root (see `.env.example`):

```env
DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:5432/kanban_db
SECRET_KEY=your_secret_key_here
```

### 4. Database Migrations
Run Alembic migrations to create tables:

```bash
alembic upgrade head
```

### 5. Running the Application
Start the Uvicorn development server:

```bash
uvicorn app.main:app --reload
```

- Web UI: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (redirects to login)
- Interactive API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

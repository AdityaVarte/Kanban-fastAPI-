$ErrorActionPreference = "Stop"

Write-Host "Setting up Kanban API project in $PWD..." -ForegroundColor Cyan

# 1. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Upgrade pip
python -m pip install --upgrade pip

# 3. Install core dependencies
pip install fastapi "uvicorn[standard]" sqlalchemy asyncpg pydantic-settings python-dotenv

# 4. Freeze dependencies
pip freeze > requirements.txt

# 5. Create folder structure
New-Item -ItemType Directory -Force -Path app\core, app\db, app\models, app\schemas, app\routers | Out-Null

# 6. Create __init__.py files
New-Item -ItemType File -Force -Path app\__init__.py, app\core\__init__.py, app\db\__init__.py, app\models\__init__.py, app\schemas\__init__.py, app\routers\__init__.py | Out-Null

# 7. Create config, session placeholder files
New-Item -ItemType File -Force -Path app\core\config.py, app\db\session.py | Out-Null

# 8. Create .env with placeholder DB URL
@"
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/kanban_db
"@ | Out-File -FilePath .env -Encoding utf8

# 9. Create .gitignore
@"
venv/
__pycache__/
*.pyc
.env
"@ | Out-File -FilePath .gitignore -Encoding utf8

# 10. Create main.py
@"
from fastapi import FastAPI

app = FastAPI(title="Kanban Board API")

@app.get("/")
async def root():
    return {"message": "Kanban API is running"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
"@ | Out-File -FilePath app\main.py -Encoding utf8

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "Activate your venv (if not already): .\venv\Scripts\Activate.ps1"
Write-Host "Run the server: uvicorn app.main:app --reload"
Write-Host "Then visit: http://127.0.0.1:8000/docs"
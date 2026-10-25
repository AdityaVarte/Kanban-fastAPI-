from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.routers import boards, columns, cards, auth

app = FastAPI(title="Kanban Board API")

app.include_router(auth.router)
app.include_router(boards.router)
app.include_router(columns.router)
app.include_router(cards.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/static/login.html")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
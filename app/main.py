from fastapi import FastAPI
from alembic import command
from alembic.config import Config
import os
from app.api.routes.auth import router as auth_router
import app.db.imports
from app.api.routes.me import router as me_router
from app.api.routes.tasks import router as task_router
app =FastAPI(
    title="task service api",
    version="0.1.0"
)
@app.on_event("startup")
async def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        os.environ["DATABASE_URL"],
    )
    command.upgrade(alembic_cfg, "head")

app.include_router(auth_router)
app.include_router(me_router)
app.include_router(task_router)

@app.get("/",tags=["root"])
async def health_check():
    return {"project":"user_backend"}

@app.get("/health",tags=["health"])
async def health_check():
    return {"status":"ok"}
from __future__ import annotations
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .routers import action_items, notes
from .services.db import init_db

# --- TODO 3: Refactor App Lifecycle ---
# Menggunakan asynccontextmanager untuk inisialisasi database saat aplikasi dimulai.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO 3: Database layer cleanup - initialize DB on startup
    init_db()
    yield

app = FastAPI(
    title="Action Item Extractor",
    lifespan=lifespan
)

@app.get("/", response_class=HTMLResponse)
def index() -> str:
    html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    return html_path.read_text(encoding="utf-8")

# Include Routers
app.include_router(notes.router)
app.include_router(action_items.router)

# Static Files
static_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
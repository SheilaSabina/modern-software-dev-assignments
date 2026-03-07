import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import iterate_in_threadpool

from .db import apply_seed_if_needed, engine
from .models import Base
from .routers import action_items as action_items_router
from .routers import notes as notes_router

app = FastAPI(title="Modern Software Dev Starter (Week 5)")

# Ensure data dir exists
Path("data").mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "ok": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
            },
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "ok": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(exc.errors()),
            },
        },
    )


# ---------------------------------------------------------------------------
# Response envelope middleware
# ---------------------------------------------------------------------------
EXCLUDED_PATHS = ("/", "/docs", "/openapi.json")


@app.middleware("http")
async def response_envelope_middleware(request: Request, call_next):
    path = request.url.path

    # Skip excluded paths and static files
    if path in EXCLUDED_PATHS or path.startswith("/static"):
        return await call_next(request)

    response = await call_next(request)

    # Only wrap successful responses (2xx)
    if 200 <= response.status_code <= 299:
        body_chunks = []
        async for chunk in response.body_iterator:
            if isinstance(chunk, str):
                body_chunks.append(chunk.encode("utf-8"))
            else:
                body_chunks.append(chunk)
        body = b"".join(body_chunks)

        try:
            data = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return response

        wrapped = {"ok": True, "data": data}
        return JSONResponse(
            status_code=response.status_code,
            content=wrapped,
        )

    return response


# ---------------------------------------------------------------------------
# Startup & routes
# ---------------------------------------------------------------------------
@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)
    apply_seed_if_needed()


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("frontend/index.html")


# Routers
app.include_router(notes_router.router)
app.include_router(action_items_router.router)

# Mount static frontend (AFTER routers so /static doesn't shadow API routes)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.routes import contacts, auth, users
import os
from pathlib import Path
from dependencies import get_redis_client
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

app = FastAPI()
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)

app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """
    Initialize FastAPI requests limiter
    """
    await FastAPILimiter.init(get_redis_client())


@app.get("/")
def read_root():
    """
    root level endpoint

    :return: Hello world message.
    :rtype: dict
    """

    return {"message": "Hello world"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Endpoint to serve the favicon.

    :return: The favicon file.
    :rtype: FileResponse
    """
    file_name = "favicon.png"
    file_path = os.path.join(app.root_path, "static", file_name)
    return FileResponse(
        path=file_path,
        headers={"Content-Disposition": "attachment; filename=" + file_name},
    )

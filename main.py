from fastapi import FastAPI, Path, Depends, HTTPException, status, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.repository.abstract import AbstractContactRepository
from src.schemas.contacts import ContactOut, ContactIn
from src.routes import contacts
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(contacts.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Hello world"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    file_name = "favicon.png"
    file_path = os.path.join(app.root_path, "static", file_name)
    return FileResponse(
        path=file_path,
        headers={"Content-Disposition": "attachment; filename=" + file_name},
    )

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.routes import contacts, auth
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")


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

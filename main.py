from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from redis import Redis
from src.config import settings
from src.routes import contacts, auth, users
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")


# @app.on_event("startup")
# async def startup():
#     redis = Redis(
#         host=settings.redis_host,
#         port=settings.redis_port,
#         db=0,
#         encoding="utf-8",
#         decode_responses=True,
#     )
#     await FastAPILimiter.init(redis)


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

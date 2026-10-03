from fastapi import FastAPI
from app.routers.user import router as auth_router
from app.routers.application import router as application_router


app = FastAPI()


app.include_router(auth_router, tags=["Auth"])
app.include_router(application_router, tags=["Application"])
from fastapi import FastAPI
from app.routers.user import router as auth_router


app = FastAPI()


app.include_router(auth_router, tags=["Auth"])

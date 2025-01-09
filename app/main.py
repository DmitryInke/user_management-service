from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import auth, user
from app.db.init_db import engine
from app.db.base import Base
from app.middleware.auth_middleware import AuthMiddleware

app = FastAPI(title="User Management Service",
              version="1.0.0")


@asynccontextmanager
async def lifespan():
    print("Starting up the application...")
    Base.metadata.create_all(bind=engine)
    yield
    print("Shutting down the application...")


app.add_middleware(AuthMiddleware)
app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")


@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "User Management Service is running"}

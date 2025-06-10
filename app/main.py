from fastapi import FastAPI
from app.users.router import router as users_router
from app.entries.router import router as entries_router

app = FastAPI()

app.include_router(users_router)
app.include_router(entries_router)
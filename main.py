from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import admin_routes, login_router, user_router, webhook_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)
app.include_router(user_router)
app.include_router(admin_routes)
app.include_router(webhook_router)


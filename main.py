from fastapi import FastAPI

from api import admin_routes, login_router, user_router

app = FastAPI()

app.include_router(login_router)
app.include_router(user_router)
app.include_router(admin_routes)


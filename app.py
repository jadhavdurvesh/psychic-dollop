from fastapi import FastAPI

from src.redirect_route import router as redirect_router
from src.shorten_route import router as shorten_router

app = FastAPI()

# Register routers.
app.include_router(redirect_router)
app.include_router(shorten_router)
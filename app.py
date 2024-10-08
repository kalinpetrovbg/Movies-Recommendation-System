# app.py

import logging

import uvicorn
from fastapi import FastAPI

from endpoints.api import router as api_router
from endpoints.views import router as views_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(views_router)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8828)

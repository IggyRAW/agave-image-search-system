import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.endpoints.get_named import router as named_router
from api.endpoints.get_providers import router as providers_router
from api.endpoints.search import router as search_router

app = FastAPI()

app.include_router(named_router)
app.include_router(search_router)
app.include_router(providers_router)

app.mount(
    "/images",
    StaticFiles(directory=os.path.abspath("images")),
    name="images",
)

import os
from logging import getLogger

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.endpoints.get_feature import router as feature_router
from api.endpoints.get_named import router as named_router
from api.endpoints.get_providers import router as providers_router
from api.endpoints.init import router as init_router
from api.endpoints.post_agave_obj import router as post_agave_router
from api.endpoints.search import router as search_router
from lib.log_manager import initLogger

initLogger(__file__)
logger = getLogger(__name__)

app = FastAPI()

app.include_router(named_router)
app.include_router(search_router)
app.include_router(providers_router)
app.include_router(post_agave_router)
app.include_router(init_router)
app.include_router(feature_router)

app.mount(
    "/images",
    StaticFiles(directory=os.path.abspath("images")),
    name="images",
)

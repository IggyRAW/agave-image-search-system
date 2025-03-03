from logging import getLogger

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.schemas.provider import Provider
from manager.config_manager import ConfigManager
from manager.es_manager import ElasticsearchManager, get_elasticsearch_manager
from query_builder.es_query_builder import ESQueryBuilder

logger = getLogger(__name__)

router = APIRouter()

config = ConfigManager()


@router.get("/get/providers")
def get_providers(
    es: ElasticsearchManager = Depends(get_elasticsearch_manager),
):
    try:
        providers = []
        query_builder = ESQueryBuilder()
        query_builder.match_all()
        response = es.search(config.AGAVE_INDEX, query_builder.build())
        response = response["hits"]["hits"]
        for res in response:
            if not Provider(username=res["_source"]["username"]) in providers:
                providers.append(Provider(username=res["_source"]["username"]))

        return providers

    except Exception:
        import traceback

        logger.error(traceback.format_exc())

        JSONResponse(
            status_code=500, content={"message": str(traceback.format_exc())}
        )

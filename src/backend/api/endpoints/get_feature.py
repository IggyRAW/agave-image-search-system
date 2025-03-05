from logging import getLogger

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from manager.config_manager import ConfigManager
from manager.es_manager import ElasticsearchManager, get_elasticsearch_manager
from query_builder.es_query_builder import ESQueryBuilder

logger = getLogger(__name__)

router = APIRouter()

config = ConfigManager()


@router.get("/get/feature")
def get_feature(
    search_word: str,
    es: ElasticsearchManager = Depends(get_elasticsearch_manager),
):
    """
    特徴を取得するAPI
    """
    try:
        logger.info(f"検索特徴ネーム：{search_word}")
        query_builder = ESQueryBuilder()
        query_builder.set_name_term(search_word)
        response = es.search(config.AGAVE_FEATURE_INDEX, query_builder.build())
        response = response["hits"]["hits"]
        if response:
            return response[0]["_source"]["feature"]
        else:
            return ""

    except Exception:
        import traceback

        logger.error(traceback.format_exc())

        JSONResponse(
            status_code=500, content={"message": str(traceback.format_exc())}
        )

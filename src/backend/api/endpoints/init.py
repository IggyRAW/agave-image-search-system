from logging import getLogger

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from manager.config_manager import ConfigManager
from manager.es_manager import ElasticsearchManager, get_elasticsearch_manager
from query_builder.es_query_builder import ESQueryBuilder

logger = getLogger(__name__)

router = APIRouter()

config = ConfigManager()


@router.get("/init")
def init(es: ElasticsearchManager = Depends(get_elasticsearch_manager)):
    try:
        query_builder = ESQueryBuilder()
        query_builder.match_all()
        query_builder.set_sort("search_count", "desc")
        response = es.search(config.SEARCH_COUNT_INDEX, query_builder.build())

        ranking_list = []
        for res in response["hits"]["hits"]:
            if not res["_source"]["name"] in ranking_list:
                ranking_list.append(res["_source"]["name"])

            # 上位5位取得して抜ける
            if len(ranking_list) > 4:
                break

        return {"ranking_list": ranking_list}

    except Exception:
        import traceback

        logger.error(traceback.format_exc())

        JSONResponse(
            status_code=500, content={"message": str(traceback.format_exc())}
        )

from logging import getLogger

from elasticsearch.helpers import bulk
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.schemas.search import CardItemModel
from lib.utils import update_search_count
from manager.config_manager import ConfigManager
from manager.es_manager import ElasticsearchManager, get_elasticsearch_manager
from query_builder.es_query_builder import ESQueryBuilder

logger = getLogger(__name__)

router = APIRouter()

config = ConfigManager()


@router.get("/search")
async def search(
    search_word: str,
    page: int = 1,
    limit: int = 18,
    es: ElasticsearchManager = Depends(get_elasticsearch_manager),
):
    """
    検索API
    """
    try:
        logger.info(
            f"検索ワード：{search_word} ページ：{page} リミット：{limit}"
        )
        offset = (page - 1) * limit
        query_builder = ESQueryBuilder()
        if search_word:
            query_builder.set_bool()
            query_builder.set_should()
            query_builder.create_search_name_query("name", search_word)
        else:
            query_builder.match_all()

        query = query_builder.build()
        query["from"] = offset
        query["size"] = limit

        response = es.search(config.AGAVE_INDEX, query)
        total = response["hits"]["total"]["value"]
        response = response["hits"]["hits"]

        search_list = []
        for res in response:
            search_list.append(
                CardItemModel(
                    id=res["_id"],
                    name=res["_source"]["name"],
                    username=res["_source"]["username"],
                    username_source=res["_source"]["username_source"],
                    image_file_path=res["_source"]["image_file_path"],
                    source=res["_source"]["source"],
                    sourcename=res["_source"]["sourcename"],
                    image_source=res["_source"]["image_source"],
                    origin_country=res["_source"]["origin_country"],
                )
            )

        if page == 1:
            update_search_count(search_word, es)

        return {
            "total": total,
            "search_list": search_list,
        }

    except Exception:
        import traceback

        logger.error(traceback.format_exc())

        JSONResponse(
            status_code=500, content={"message": str(traceback.format_exc())}
        )


@router.get("/search_provider")
def search_providers(
    provider: str,
    page: int = 1,
    limit: int = 18,
    es: ElasticsearchManager = Depends(get_elasticsearch_manager),
):
    """
    検索API
    """
    try:
        logger.info(f"提供者名：{provider} ページ：{page} リミット：{limit}")
        offset = (page - 1) * limit
        query_builder = ESQueryBuilder()

        if provider:
            query_builder.set_username_term(provider)
        else:
            query_builder.match_all()

        query = query_builder.build()
        query["from"] = offset
        query["size"] = limit

        response = es.search(config.AGAVE_INDEX, query)
        total = response["hits"]["total"]["value"]
        response = response["hits"]["hits"]

        search_list = [
            CardItemModel(
                id=res["_id"],
                name=res["_source"]["name"],
                username=res["_source"]["username"],
                username_source=res["_source"]["username_source"],
                image_file_path=res["_source"]["image_file_path"],
                source=res["_source"]["source"],
                sourcename=res["_source"]["sourcename"],
                image_source=res["_source"]["image_source"],
                origin_country=res["_source"]["origin_country"],
            )
            for res in response
        ]
        return {
            "total": total,
            "search_list": search_list,
        }

    except Exception:
        import traceback

        logger.error(traceback.format_exc())

        JSONResponse(
            status_code=500, content={"message": str(traceback.format_exc())}
        )

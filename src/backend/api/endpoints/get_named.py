from logging import getLogger

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.schemas.named import Named
from api.schemas.search import CardItemModel
from lib.utils import update_search_count
from manager.config_manager import ConfigManager
from manager.es_manager import ElasticsearchManager, get_elasticsearch_manager
from query_builder.es_query_builder import ESQueryBuilder

logger = getLogger(__name__)

router = APIRouter()

config = ConfigManager()


@router.get("/get/named/list")
def get_named_list(
    es: ElasticsearchManager = Depends(get_elasticsearch_manager),
):
    try:
        named_list = []
        query_builder = ESQueryBuilder()
        query_builder.match_all()
        response = es.search(config.AGAVE_INDEX, query_builder.build())
        response = response["hits"]["hits"]
        for res in response:
            if not Named(name=res["_source"]["name"]) in named_list:
                named_list.append(Named(name=res["_source"]["name"]))

        return named_list

    except Exception:
        import traceback

        logger.error(traceback.format_exc())

        JSONResponse(
            status_code=500, content={"message": str(traceback.format_exc())}
        )


@router.get("/get/named/search")
def search_named(
    search_word: str,
    page: int = 1,
    limit: int = 18,
    es: ElasticsearchManager = Depends(get_elasticsearch_manager),
):
    try:
        logger.info(
            f"ネームド名：{search_word} ページ：{page} リミット：{limit}"
        )
        offset = (page - 1) * limit
        query_builder = ESQueryBuilder()
        if search_word:
            query_builder.set_name_term(search_word)
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

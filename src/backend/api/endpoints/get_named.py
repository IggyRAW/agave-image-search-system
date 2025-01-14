from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.schemas.named import Named
from api.schemas.search import CardItemModel
from manager.es_manager import ElasticsearchManager, get_elasticsearch_manager
from query_builder.es_query_builder import ESQueryBuilder

router = APIRouter()


@router.get("/get/named/list")
def get_named_list(
    es: ElasticsearchManager = Depends(get_elasticsearch_manager),
):
    try:
        named_list = []
        query_builder = ESQueryBuilder()
        query_builder.match_all()
        response = es.search(query_builder.build())
        response = response["hits"]["hits"]
        for res in response:
            if not Named(name=res["_source"]["name"]) in named_list:
                named_list.append(Named(name=res["_source"]["name"]))

        return named_list

    except Exception:
        import traceback

        JSONResponse(
            status_code=500, content={"message": str(traceback.format_exc())}
        )


@router.get("/get/named/search")
def search_named(
    search_word: str,
    es: ElasticsearchManager = Depends(get_elasticsearch_manager),
):
    try:
        if search_word:
            query_builder = ESQueryBuilder()
            query_builder.set_name_term(search_word)
            response = es.search(query_builder.build())
            response = response["hits"]["hits"]
            if len(response):
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
            else:
                search_list = []
        else:
            query_builder = ESQueryBuilder()
            query_builder.match_all()
            response = es.search(query_builder.build())
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
        return search_list

    except Exception:
        import traceback

        JSONResponse(
            status_code=500, content={"message": str(traceback.format_exc())}
        )

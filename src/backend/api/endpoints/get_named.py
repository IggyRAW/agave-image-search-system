from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.schemas.named import Named
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

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from manager.es_manager import ElasticsearchManager, get_elasticsearch_manager
from query_builder.es_query_builder import ESQueryBuilder

router = APIRouter()


@router.get("/init")
def init(es: ElasticsearchManager = Depends(get_elasticsearch_manager)):
    try:
        query_builder = ESQueryBuilder()
        query_builder.match_all()
        query_builder.set_sort("search_count", "desc")
        response = es.search(query_builder.build())

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

        print(traceback.format_exc())

        JSONResponse(
            status_code=500, content={"message": str(traceback.format_exc())}
        )

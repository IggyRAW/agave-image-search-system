import math
import os

import pandas as pd
from elasticsearch.helpers import bulk
from tqdm import tqdm

from manager.config_manager import ConfigManager
from manager.es_manager import ElasticsearchManager
from query_builder.es_query_builder import ESQueryBuilder

es = ElasticsearchManager(1)

config = ConfigManager()


def import_data():
    try:
        df = _load_excel(_get_excel_file(config.EXCEL))
        named_list = []
        bulk_data = []
        for row in tqdm(df.itertuples()):
            if row.name not in named_list:
                named_list.append(row.name)
            # 原産国がNaNの場合Noneに変換
            origin_country = (
                None
                if isinstance(row.origin_country, float)
                and math.isnan(row.origin_country)
                else row.origin_country
            )

            # image_sourceがNaNの場合Noneに変換
            image_source = (
                None
                if isinstance(row.image_source, float)
                and math.isnan(row.image_source)
                else row.image_source
            )
            doc = {
                "_index": config.AGAVE_INDEX,
                "_source": {
                    "name": row.name,
                    "username": row.username,
                    "username_source": row.username_source,
                    "image_file_path": row.image_file_path,
                    "source": row.source,
                    "sourcename": row.sourcename,
                    "image_source": image_source,
                    "origin_country": origin_country,
                    "is_display": row.is_display,
                },
            }

            builder = ESQueryBuilder()
            builder.set_bool()
            builder.set_should()
            builder.create_search_name_query("name", row.name)
            response = es.search(config.AGAVE_INDEX, builder.build())
            if _check_doc(response["hits"]["hits"], doc["_source"]):
                bulk_data.append(doc)

        if bulk_data:
            success, failed = bulk(es.es, bulk_data)
            print(f"{success}件のデータを{config.AGAVE_INDEX}に格納しました。")
            bulk_data = []

        # search_count_indexの作成
        query_builder_for_search_count = ESQueryBuilder()
        query_builder_for_search_count.match_all()
        response = es.search(
            config.SEARCH_COUNT_INDEX, query_builder_for_search_count.build()
        )
        response = response["hits"]["hits"]
        for named in tqdm(named_list):
            if any(named == res["_source"]["name"] for res in response):
                continue
            doc = {
                "_index": config.SEARCH_COUNT_INDEX,
                "_source": {"name": named, "search_count": 0},
            }
            bulk_data.append(doc)

        if bulk_data:
            success, failed = bulk(es.es, bulk_data)
            print(
                f"{success}件のデータを{config.SEARCH_COUNT_INDEX}に格納しました。"
            )
            bulk_data = []

    except Exception:
        raise


def _get_excel_file(path: str, extensions=("xlsx")):
    if not os.path.isdir(path):
        raise FileNotFoundError(f"指定されたフォルダが見つかりません：{path}")
    file = os.listdir(path)
    if len(file) != 1:
        raise ValueError("Excelフォルダには1つのファイルが必要です")
    if not file[0].lower().endswith(extensions):
        raise ValueError("Excelファイルとは異なるファイルはロードできません。")
    return os.path.join(path, file[0])


def _load_excel(path: str):
    return pd.read_excel(path, sheet_name="Sheet1", engine="openpyxl")


def _check_doc(response, doc: dict) -> bool:
    for res in response:
        if doc == res["_source"]:
            return False
    return True


if __name__ == "__main__":
    try:
        print("---------------start import data---------------")
        import_data()
        print("---------------end import data---------------")

    except Exception:
        import traceback

        print(traceback.format_exc())

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


def import_feature():
    try:
        df = _load_excel(_get_excel_file(config.EXCEL))
        bulk_data = []
        for row in tqdm(df.itertuples()):
            # featureがNaNの場合空文字に変換
            leaf_color = (
                ""
                if isinstance(row.leaf_color, float)
                and math.isnan(row.leaf_color)
                else row.leaf_color
            )
            leaf_type = (
                ""
                if isinstance(row.leaf_type, float)
                and math.isnan(row.leaf_type)
                else row.leaf_type
            )
            spine_color = (
                ""
                if isinstance(row.spine_color, float)
                and math.isnan(row.spine_color)
                else row.spine_color
            )

            spine_types = [
                s
                for s in [row.spine_type, row._6, row._7]
                if not (isinstance(s, float) and math.isnan(s))
            ]

            doc = {
                "_index": config.AGAVE_FEATURE_INDEX,
                "_source": {
                    "name": row.name,
                    "leaf_color": leaf_color,
                    "leaf_type": leaf_type,
                    "spine_color": spine_color,
                    "spine_type": spine_types,
                },
            }

            builder = ESQueryBuilder()
            builder.set_name_term(row.name)
            # builder.set_bool()
            # builder.set_should()
            # builder.create_search_name_query("name", row.name)
            response = es.search(config.AGAVE_FEATURE_INDEX, builder.build())
            if _check_doc(response["hits"]["hits"], doc["_source"]):
                bulk_data.append(doc)

        if bulk_data:
            success, _ = bulk(es.es, bulk_data)
            print(
                f"{success}件のデータを{config.AGAVE_FEATURE_INDEX}に格納しました。"
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
    return pd.read_excel(path, sheet_name="Sheet3", engine="openpyxl")


def _check_doc(response, doc: dict) -> bool:
    for res in response:
        if doc == res["_source"]:
            return False
    return True


if __name__ == "__main__":
    try:
        print("---------------start import data---------------")
        import_feature()
        print("---------------end import data---------------")

    except Exception:
        import traceback

        print(traceback.format_exc())

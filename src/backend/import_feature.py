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
            feature = (
                ""
                if isinstance(row.feature, float) and math.isnan(row.feature)
                else row.feature
            )
            doc = {
                "_index": config.AGAVE_FEATURE_INDEX,
                "_source": {
                    "name": row.name,
                    "feature": feature,
                },
            }

            builder = ESQueryBuilder()
            builder.set_bool()
            builder.set_should()
            builder.create_search_name_query("name", row.name)
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
    return pd.read_excel(path, sheet_name="Sheet2", engine="openpyxl")


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

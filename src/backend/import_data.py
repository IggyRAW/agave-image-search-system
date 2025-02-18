import math
import os
from typing import Optional

import pandas as pd

from manager.config_manager import ConfigManager
from manager.es_manager import ElasticsearchManager
from query_builder.es_query_builder import ESQueryBuilder

es = ElasticsearchManager()


class CardItemModel:
    def __init__(
        self,
        name: str,
        username: str,
        username_source: str,
        image_file_path: str,
        source: str,
        sourcename: str,
        image_source: str,
        origin_country: Optional[str] = None,
        is_display: bool = True,
        search_count: int = 0,
    ):
        self.name = name
        self.username = username
        self.username_source = username_source
        self.image_file_path = image_file_path
        self.source = source
        self.sourcename = sourcename
        self.image_source = image_source
        self.origin_country = origin_country
        self.is_display = is_display
        self.search_count = search_count


def import_data():
    try:
        df = _load_excel(_get_excel_file(ConfigManager().EXCEL))
        for row in df.itertuples():
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
            doc = CardItemModel(
                name=row.name,
                username=row.username,
                username_source=row.username_source,
                image_file_path=row.image_file_path,
                source=row.source,
                sourcename=row.sourcename,
                image_source=image_source,
                origin_country=origin_country,
                is_display=row.is_display,
                search_count=row.search_count,
            ).__dict__

            builder = ESQueryBuilder()
            builder.set_bool()
            builder.set_should()
            builder.create_search_name_query("name", row.name)
            response = es.search(builder.build())
            if _check_doc(response["hits"]["hits"], doc):
                es.insert(doc)
                print(f"{row.name}を格納しました。")

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

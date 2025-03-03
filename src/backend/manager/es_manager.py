from logging import getLogger

from elasticsearch import Elasticsearch

from manager.config_manager import ConfigManager

logger = getLogger(__name__)

config = ConfigManager()


class ElasticsearchManager:
    def __init__(self, mode: int = 0):
        if mode != 0:
            self.es = Elasticsearch(
                hosts=f"http://localhost:{config.ES_PORT}",
                verify_certs=False,
                timeout=30,
            )
        else:
            self.es = Elasticsearch(
                # hosts=f"http://{config.ES_HOST}:{config.ES_PORT}",
                hosts=f"http://localhost:{config.ES_PORT}",
                verify_certs=False,
                timeout=30,
            )
        self.create_index()

    def create_index(self):
        """
        インデックス作成
        """
        indices = [config.AGAVE_INDEX, config.SEARCH_COUNT_INDEX]
        mappings = [
            config.AGAVE_INDEX_MAPPING,
            config.SEARCH_COUNT_INDEX_MAPPING,
        ]
        for index, mapping in zip(indices, mappings):
            if not self.es.indices.exists(index=index):
                self.es.indices.create(index=index, body=mapping)
                logger.info(f"{index}を作成しました")

    def search(self, index: str, query):
        """
        検索
        """
        return self.es.search(index=index, body=query)

    def insert(self, index: str, doc: dict):
        return self.es.index(index=index, document=doc)

    def update(self, index: str, id: str, doc):
        return self.es.update(index=index, id=id, body=doc)

    def refresh(self, index: str):
        return self.es.indices.refresh(index=index)

    def close(self):
        return self.es.close()


def get_elasticsearch_manager():
    """
    ElasticSeaerchのリソースを管理するための関数
    """
    manager = ElasticsearchManager()
    try:
        yield manager
    finally:
        manager.close()

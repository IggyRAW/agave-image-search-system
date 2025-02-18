from elasticsearch import Elasticsearch

from manager.config_manager import ConfigManager

config = ConfigManager()

INDEX_NAME = "agave_index"


class ElasticsearchManager:
    def __init__(self):
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
        if not self.es.indices.exists(index=INDEX_NAME):
            self.es.indices.create(index=INDEX_NAME, body=config.MAPPING)
            print("インデックスを作成しました")

    def search(self, query):
        """
        検索
        """
        return self.es.search(index=INDEX_NAME, body=query)

    def insert(self, doc: dict):
        return self.es.index(index=INDEX_NAME, document=doc)

    def update(self, id: str, doc):
        return self.es.update(index=INDEX_NAME, id=id, body=doc)

    def refresh(self):
        return self.es.indices.refresh(index=INDEX_NAME)

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

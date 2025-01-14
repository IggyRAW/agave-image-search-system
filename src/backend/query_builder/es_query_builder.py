import copy

from manager.config_manager import ConfigManager

config = ConfigManager()


class ESQueryBuilder:
    def __init__(self):
        self.query = copy.deepcopy(config.QUERY)

    def match_all(self):
        self.query["query"]["match_all"] = {}

    def set_bool(self):
        self.query["query"]["bool"] = {}

    def set_should(self):
        self.query["query"]["bool"]["should"] = []

    def create_search_name_query(self, field: str, name: str):
        query = [{"wildcard": {field: f"*{name}*"}}, {"match": {field: name}}]
        if "should" in self.query["query"]["bool"]:
            self.query["query"]["bool"]["should"].extend(query)
        else:
            self.query["query"]["bool"]["should"] = query

    def set_name_term(self, name: str):
        self.query["query"]["term"] = {"name.keyword": name}

    def build(self):
        return self.query

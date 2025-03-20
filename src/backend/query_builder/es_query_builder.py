import copy

from manager.config_manager import ConfigManager

config = ConfigManager()


class ESQueryBuilder:
    def __init__(self):
        self.query = copy.deepcopy(config.QUERY)

    def match_all(self):
        self.query["query"]["match_all"] = {}

    def set_source(self, fields: list):
        self.query["_source"] = fields

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

    def set_term(self, field: str, term: str):
        if "bool" in self.query["query"]:
            if "should" in self.query["query"]["bool"]:
                self.query["query"]["bool"]["should"].append(
                    {"term": {f"{field}.keyword": term}}
                )
            else:
                self.set_should()
                self.query["query"]["bool"]["should"].append(
                    {"term": {f"{field}.keyword": term}}
                )
        else:
            self.query["query"]["term"] = {f"{field}.keyword": term}

    def set_terms(self, field: str, term: list):
        if "bool" in self.query["query"]:
            if "should" in self.query["query"]["bool"]:
                self.query["query"]["bool"]["should"].append(
                    {"terms": {f"{field}.keyword": term}}
                )
            else:
                self.set_should()
                self.query["query"]["bool"]["should"].append(
                    {"term": {f"{field}.keyword": term}}
                )
        else:
            self.query["query"]["terms"] = {f"{field}.keyword": term}

    def set_name_term(self, name: str):
        self.query["query"]["term"] = {"name.keyword": name}

    def set_username_term(self, username: str):
        self.query["query"]["term"] = {"username.keyword": username}

    def set_sort(self, field: str, order: str):
        self.query["sort"] = [{field: {"order": order}}]

    def build(self):
        return self.query

import commentjson

JSON_FILE_PATH = "settengs.jsonc"


class ConfigManager:
    def __init__(self):
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            json_settings = commentjson.load(file)
        self.settings = json_settings

        self.ES_HOST = self.settings.get("elasticsearch").get("host")
        self.ES_PORT = self.settings.get("elasticsearch").get("port")
        self.MAPPING = self.settings.get("mapping")
        self.QUERY = self.settings.get("query")
        self.EXCEL = self.settings.get("excel")

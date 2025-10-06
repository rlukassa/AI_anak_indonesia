import json

class JSONParser:
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def parse_section(self, key: str) -> list[dict]:
        if key not in self.data:
            raise ValueError(f"Key '{key}' missing in JSON")
        section = self.data[key]
        return section


'''
Cara pake: 
global parser = JSONParser(<absolute_path>)

parser(<KEY>) -> list of key value pairs (nanti construct initialize di class masing2)

CEK DI tests.test_json_parser
'''
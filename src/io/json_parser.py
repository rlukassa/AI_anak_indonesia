import json

class JSONParser:
    def __init__(self, path):
        """Load JSON file"""
        with open(path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def parse_section(self, key: str) -> list[dict]:
        """Extract a section from JSON"""
        if key not in self.data:
            raise ValueError(f"Key '{key}' missing in JSON")
        return self.data[key]

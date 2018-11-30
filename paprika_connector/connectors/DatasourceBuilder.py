import json
import os
from paprika_connector.system.Finder import Finder


class DatasourceBuilder:
    def __init__(self):
        pass

    @staticmethod
    def build(filename, default=None):
        env = os.environ.get("ENVIRONMENT", "dev")
        f = Finder.open(filename, default)
        data = json.load(f)
        f.close()
        return data[env]
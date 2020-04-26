
import pandas as pd

class DataSource:
    SOURCE_DATA_PATH = None
    SOURCE_TABLES = None
    SOURCE_URLS = None

    def __init__(self, data_path=SOURCE_DATA_PATH, update=False):
        self.tables = self.SOURCE_TABLES
        self.update = update
        self.data_path = data_path

    def _locate_file(self, name, update=False):
        data_file = self.tables[name]
        full_path = str(self.data_path / data_file)
        logger.info("searching for file %s", full_path)

        if os.path.exists(full_path):
            return full_path
        elif os.path.exists(full_path + ".gz"):
            return full_path + ".gz"
        elif update:
            logger.info("updating file %s", full_path)
            _update_file(SOURCE_URLS[name])
            return self._locate_file(name, False)
        else:
            raise FileNotFoundError(f"Cannot find file {full_path}")

    def _load(self, name):
        file_full_path = self._locate_file(name, self.update)
        return pd.read_csv(file_full_path)

    def __getattr__(self, name):
        if name not in self.tables.keys():
            raise AttributeError
        try:
            self.__dict__[name] = self._load(name)
            return self.__dict__[name]
        except FileNotFoundError:
            raise AttributeError

import pandas as pd

class MovieData:
    _instance = None

    @classmethod
    def get_instance(cls, file_path):
        if cls._instance is None:
            cls._instance = cls(file_path)
        return cls._instance

    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

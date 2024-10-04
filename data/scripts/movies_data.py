import pandas as pd

class MovieData:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

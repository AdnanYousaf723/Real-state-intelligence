import pandas as pd
from .base import DataSource

class CSVDataSource(DataSource):
    def __init__(self, file_path: str, source_name: str = "sample_csv"):
        self.file_path = file_path
        self.source_name = source_name

    def fetch(self) -> pd.DataFrame:
        """Reads raw data from CSV and returns a pandas DataFrame."""
        try:
            df = pd.read_csv(self.file_path, dtype=str)
            # Replace nan strings or pandas NA with empty string to help validation
            df = df.fillna("")
            return df
        except Exception as e:
            # Return empty dataframe with expected columns if file fails
            return pd.DataFrame()

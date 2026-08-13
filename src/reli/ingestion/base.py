import pandas as pd

class DataSource:
    def fetch(self) -> pd.DataFrame:
        raise NotImplementedError

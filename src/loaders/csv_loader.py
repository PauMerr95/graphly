from pathlib import Path

import pandas as pd

from loaders.base import DataLoader


class CSVLoader(DataLoader):
    def load(self, path: Path) -> pd.DataFrame:
        if not path.exists():
            raise ValueError(f'Specified datafile at "{path}" does not exist')
        data = pd.read_csv(path, skipinitialspace=True)
        data.columns = data.columns.str.strip()
        return data

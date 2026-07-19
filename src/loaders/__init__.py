from pathlib import Path

import pandas as pd

from loaders.base import DataLoader as DataLoader
from loaders.csv_loader import CSVLoader as CSVLoader

_LOADERS: dict[str, DataLoader] = {
    ".csv": CSVLoader(),
}


def load_datafile(path: Path) -> pd.DataFrame:
    loader = _LOADERS.get(path.suffix)
    if loader is None:
        raise ValueError(f'Unsupported datafile type "{path.suffix}" for "{path}"')
    return loader.load(path)

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class DataLoader(ABC):
    @abstractmethod
    def load(self, path: Path) -> pd.DataFrame: ...

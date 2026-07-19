from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

from config.parser import Config


class Plotter(ABC):
    @abstractmethod
    def render(self, data: pd.DataFrame, config: Config) -> Any: ...

    @abstractmethod
    def show(self, figure: Any) -> None: ...

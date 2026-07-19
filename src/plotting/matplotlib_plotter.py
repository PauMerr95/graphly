import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from config.parser import Config
from plotting.base import Plotter

_DPI = 100
_THEME_STYLES = {
    "Default": "default",
    "Seaborn": "seaborn-v0_8",
}


class MatplotlibPlotter(Plotter):
    def render(self, data: pd.DataFrame, config: Config) -> Figure:
        width = config.ir_data.override_width or config.general.width
        height = config.ir_data.override_height or config.general.height
        style = _THEME_STYLES[config.general.theme]

        with plt.style.context(style):
            fig, ax = plt.subplots(figsize=(width / _DPI, height / _DPI))
            ax.plot(data["Wavenumber"], data["Transmittance"])
            ax.set_xlabel("Wavenumber")
            ax.set_ylabel("Transmittance")
            ax.get_yaxis().set_visible(config.ir_data.y_axis == "visible")

        return fig

    def show(self, figure: Figure) -> None:
        plt.show()

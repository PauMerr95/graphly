from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")

from config.parser import build_default_config, import_config_toml
from loaders import load_datafile
from plotting.matplotlib_plotter import MatplotlibPlotter

TEST_DATA = Path(__file__).parent.parent / "test_data"


class TestMatplotlibPlotter:
    def test_render_uses_general_dimensions(self):
        config = build_default_config()
        data = load_datafile(TEST_DATA / "ir_spectra_data - Molecule 1-2.csv")

        figure = MatplotlibPlotter().render(data, config)

        assert tuple(figure.get_size_inches()) == (6.0, 4.0)

    def test_render_applies_override_dimensions(self):
        config = import_config_toml(TEST_DATA / "graphly.config.toml")
        config.ir_data.override_width = 500
        config.ir_data.override_height = 300
        data = load_datafile(TEST_DATA / "ir_spectra_data - Molecule 1-2.csv")

        figure = MatplotlibPlotter().render(data, config)

        assert tuple(figure.get_size_inches()) == (5.0, 3.0)

    def test_render_hides_y_axis_when_configured_hidden(self):
        config = build_default_config()
        assert config.ir_data.y_axis == "hidden"
        data = load_datafile(TEST_DATA / "ir_spectra_data - Molecule 1-2.csv")

        figure = MatplotlibPlotter().render(data, config)

        assert figure.axes[0].get_yaxis().get_visible() is False

    def test_render_shows_y_axis_when_configured_visible(self):
        config = build_default_config()
        config.ir_data.y_axis = "visible"
        data = load_datafile(TEST_DATA / "ir_spectra_data - Molecule 1-2.csv")

        figure = MatplotlibPlotter().render(data, config)

        assert figure.axes[0].get_yaxis().get_visible() is True

    def test_render_plots_wavenumber_against_transmittance(self):
        config = build_default_config()
        data = load_datafile(TEST_DATA / "ir_spectra_data - Molecule 1-2.csv")

        figure = MatplotlibPlotter().render(data, config)

        (line,) = figure.axes[0].get_lines()
        assert np.asarray(line.get_xdata()).tolist() == list(data["Wavenumber"])
        assert np.asarray(line.get_ydata()).tolist() == list(data["Transmittance"])

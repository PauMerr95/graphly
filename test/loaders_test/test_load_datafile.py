from pathlib import Path

import pytest
from loaders import load_datafile

TEST_DATA = Path(__file__).parent.parent / "test_data"


class TestLoadDatafile:
    def test_dispatches_csv_to_csv_loader(self):
        data = load_datafile(TEST_DATA / "ir_spectra_data - Molecule 1-2.csv")
        assert list(data.columns) == ["Wavenumber", "Transmittance"]

    def test_unsupported_suffix_raises(self):
        with pytest.raises(ValueError):
            load_datafile(TEST_DATA / "graphly.config.toml")

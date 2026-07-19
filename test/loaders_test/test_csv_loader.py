from pathlib import Path

import pytest
from loaders.csv_loader import CSVLoader

TEST_DATA = Path(__file__).parent.parent / "test_data"


class TestCSVLoader:
    def test_loads_ir_spectrum_csv(self):
        data = CSVLoader().load(TEST_DATA / "ir_spectra_data - Molecule 1-2.csv")
        assert list(data.columns) == ["Wavenumber", "Transmittance"]
        assert len(data) == 62
        assert data["Wavenumber"].iloc[0] == 4000
        assert data["Transmittance"].iloc[0] == 98

    def test_missing_file_raises(self):
        with pytest.raises(ValueError):
            CSVLoader().load(TEST_DATA / "does_not_exist.csv")

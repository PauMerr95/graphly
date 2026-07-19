import sys
from pathlib import Path

import pytest
from unittest.mock import patch
from config.parser import build_default_config, import_config_toml, parse_args

TEST_DATA = Path(__file__).parent.parent / "test_data"


class TestBuildParser:
    def test_filename_only(self):
        test_args = ["graphly", "myfile.txt"]
        with patch.object(sys, "argv", test_args):
            args = parse_args()
        assert args.filename == "myfile.txt"
        assert args.config is None

    def test_with_config_flag_long(self):
        test_args = ["graphly", "myfile.txt", "--config", "config.yaml"]
        with patch.object(sys, "argv", test_args):
            args = parse_args()
        assert args.filename == "myfile.txt"
        assert args.config == "config.yaml"

    def test_with_config_flag_short(self):
        test_args = ["graphly", "myfile.txt", "-c", "config.yaml"]
        with patch.object(sys, "argv", test_args):
            args = parse_args()
        assert args.filename == "myfile.txt"
        assert args.config == "config.yaml"

    def test_missing_filename(self):
        test_args = ["graphly"]
        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit):
                parse_args()


class TestImportConfigToml:
    def test_loads_sample_config(self):
        config = import_config_toml(TEST_DATA / "graphly.config.toml")
        assert config.general.width == 600
        assert config.general.height == 400
        assert config.general.theme == "Default"
        assert config.ir_data.y_axis == "hidden"
        assert config.ir_data.spectra_spread is True
        assert config.ms_data.y_axis == "visible"
        assert config.ms_data.override_width == 500

    def test_missing_file_raises(self):
        with pytest.raises(ValueError):
            import_config_toml(TEST_DATA / "does_not_exist.toml")

    def test_non_toml_suffix_raises(self):
        with pytest.raises(ValueError):
            import_config_toml(TEST_DATA / "ir_spectra_data - Molecule 1-2.csv")


class TestBuildDefaultConfig:
    def test_matches_sample_config(self):
        default_config = build_default_config()
        sample_config = import_config_toml(TEST_DATA / "graphly.config.toml")
        assert default_config == sample_config

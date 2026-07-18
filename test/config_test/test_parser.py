import sys
import pytest
from unittest.mock import patch
from config.parser import build_parser


class TestBuildParser:
    def test_filename_only(self):
        test_args = ["graphly", "myfile.txt"]
        with patch.object(sys, "argv", test_args):
            args = build_parser()
        assert args.filename == "myfile.txt"
        assert args.config is None

    def test_with_config_flag_long(self):
        test_args = ["graphly", "myfile.txt", "--config", "config.yaml"]
        with patch.object(sys, "argv", test_args):
            args = build_parser()
        assert args.filename == "myfile.txt"
        assert args.config == "config.yaml"

    def test_with_config_flag_short(self):
        test_args = ["graphly", "myfile.txt", "-c", "config.yaml"]
        with patch.object(sys, "argv", test_args):
            args = build_parser()
        assert args.filename == "myfile.txt"
        assert args.config == "config.yaml"

    def test_missing_filename(self):
        test_args = ["graphly"]
        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit):
                build_parser()

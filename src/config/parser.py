import tomllib
import argparse
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Literal, Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="graphly",
        description="This is a quick script for building IR data graphs",
        epilog="============================================",
    )
    parser.add_argument("filename")
    parser.add_argument("-c", "--config")
    return parser.parse_args()


def generate_path(arg: str) -> Path:
    return Path(arg)


class GeneralConfig(BaseModel):
    width: int
    height: int
    theme: Literal["Default", "Seaborn"] = "Default"


class IRDataConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    override_height: Optional[int] = None
    override_width: Optional[int] = None
    y_axis: Literal["hidden", "visible"] = Field(alias="y-axis")
    spectra_spread: bool = False


class MSDataConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    override_height: Optional[int] = None
    override_width: Optional[int] = None
    y_axis: Literal["hidden", "visible"]
    spectra_spread: bool = False


class Config(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    general: GeneralConfig = Field(alias="general.config")
    ir_data: IRDataConfig = Field(alias="IR.data.config")
    ms_data: MSDataConfig = Field(alias="MS.data.config")


def build_default_config() -> Config:
    flat: dict[str, Any] = {
        "general.config": {"width": 600, "height": 400, "theme": "Default"},
        "IR.data.config": {"y_axis": "hidden", "spectra_spread": True},
        "MS.data.config": {
            "y_axis": "visible",
            "override_width": 500,
            "spectra_spread": False,
        },
    }
    return Config(**flat)


def import_config_toml(path: Path) -> Config:
    if not path.exists():
        raise ValueError(f'Specified config at "{path}" does not exist')
    if path.suffix != ".toml":
        raise ValueError(f"Specified config at \"{path}\" does not end in '.toml'")
    with path.open("rb") as file:
        data = tomllib.load(file)
    flat = {
        "general.config": data["general"]["config"],
        "IR.data.config": data["IR"]["data"]["config"],
        "MS.data.config": data["MS"]["data"]["config"],
    }
    return Config(**flat)

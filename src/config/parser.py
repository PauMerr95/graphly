import tomllib
import argparse
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Optional


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
    spectra_spread: str = Field(alias="spectra_spread")


class MSDataConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    override_height: Optional[int] = None
    override_width: Optional[int] = None
    y_axis: Literal["hidden", "visible"]
    spectra_spread: str = Field(alias="spectra_spread")


class Config(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    general: GeneralConfig = Field(alias="general.config")
    ir_data: IRDataConfig = Field(alias="IR.data.config")
    ms_data: MSDataConfig = Field(alias="MS.data.config")


def import_config_toml(path: Path) -> Config:
    if not path.exists():
        raise ValueError(f'Specified config at "{path.as_uri()}" does not exist')
    if not path.as_uri().endswith(".toml"):
        raise ValueError(
            f"Specified config at \"{path.as_uri()}\" does not end in '.toml'"
        )
    with path.open("rb") as file:
        data = tomllib.load(file)
    return Config(**data)

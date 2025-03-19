"""Global config options of the package."""

import os
from importlib import resources as pkg_resources
from pathlib import Path

from dotenv import load_dotenv

import project_name

load_dotenv()

PACKAGE_NAME = "project_name"

with pkg_resources.as_file(pkg_resources.files(project_name)) as package_dir:
    DEFAULT_CONFIG_FILE_PATH = package_dir / "logger_config.toml"

LOGGER_CONFIG_FILE = Path(os.environ.get("PROJECT_NAME_LOGGER_CONFIG_FILE", DEFAULT_CONFIG_FILE_PATH))

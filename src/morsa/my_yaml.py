from typing import Any, Union
from pathlib import Path

from yaml import safe_load


def load_yaml(path: Union[Path, str]) -> Any:
    with open(path, 'r', encoding='utf-8') as file:
        return safe_load(file)

import os
from collections.abc import Iterator

from pandas import DataFrame, concat, json_normalize


class MissingConfig(Exception):
    """Raised if a required config environment variable is not set."""


def config_from_env(key: str) -> str:
    """Fetches a config value from the global environment, raising
    MissingConfig if it isn't there.

    """
    if not (value := os.environ.get(key, None)):
        raise MissingConfig(f"{key} not set in the global environment")
    return value


def concatenate(objs: list[dict] | dict | list | Iterator) -> DataFrame:
    """
    Extend pandas concat to not only support dicts or lists of dicts, but
    also empty lists (which is often returned by the APIs).

    """
    try:
        df = concat([json_normalize(obj, sep="_") for obj in objs])
    except ValueError:
        df = DataFrame()

    return df

import os
from collections.abc import Iterator

from pandas import DataFrame
from polars import LazyFrame, concat, json_normalize

# https://github.com/astral-sh/ruff/issues/3388
from typing_extensions import Never  # noqa: UP035


class MissingConfig(Exception):
    """Raised if a required config environment variable is not set."""


def config_from_env(key: str) -> str:
    """Fetches a config value from the global environment, raising
    MissingConfig if it isn't there.

    """
    if not (value := os.environ.get(key, None)):
        raise MissingConfig(f"{key} not set in the global environment")
    return value


def concatenate(
    objs: list[dict] | dict[Never, Never] | list[Never] | Iterator,
) -> DataFrame:
    """
    Extend pandas concat to not only support dicts or lists of dicts, but
    also empty lists (which is often returned by the APIs).

    """
    try:
        df = concat([json_normalize(obj, sep="_") for obj in objs])
    except ValueError:
        df = DataFrame()

    return df


def concatenate_to_lf(
    objs: list[dict] | dict[Never, Never] | list[Never] | Iterator, schema: dict
) -> LazyFrame:
    """
    Extend Polars concat to not only support dicts or lists of dicts, but
    also empty lists (which is often returned by the APIs).

    NOTE: if you want to correctly type dates, the current workaround is
    from_dicts(list(objs), infer_schema_length=None).lazy()
    instead of concat and json_normalize
    """
    try:
        lf = concat(
            [json_normalize(obj, separator="_", schema=schema) for obj in objs]
        ).lazy()
    except ValueError:
        lf = LazyFrame(schema=schema)

    return lf

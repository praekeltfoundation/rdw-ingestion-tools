import json
import os
from collections.abc import Iterator
from io import StringIO
from itertools import chain

from polars import LazyFrame, from_dicts
from polars import json_normalize as read_json
from polars.exceptions import NoDataError

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
) -> LazyFrame:
    """
    Extend pandas concat to not only support dicts or lists of dicts, but
    also empty lists (which is often returned by the APIs).

    """
    try:
        complete_response = [obj for obj in objs]
        return from_dicts(complete_response, infer_schema_length=None).lazy()
    except NoDataError:
        df = LazyFrame()

    return df

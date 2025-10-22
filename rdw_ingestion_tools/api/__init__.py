import os
from collections.abc import Iterator

from more_itertools import chunked
from pandas import DataFrame
from pandas import json_normalize as pd_json_normalize
from polars import (
    LazyFrame,
    Object,
    String,
    col,
    concat,
    json_normalize,
)

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
        df = concat([pd_json_normalize(obj, sep="_") for obj in objs])
    except ValueError:
        df = DataFrame()

    return df


def concatenate_to_lazyframe(
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


def get_polars_schema(
    object_columns: list[str], data: list[dict[str, Object]]
) -> dict[str, Object]:
    """
    Creates a normalised LazyFrame. Returns a schema dictionary using the
    LazyFrame's column names.

    Note: Columns that are `list` types need to be type `Object` before they can be cast
    to string.
    All other column types can be cast directly to string using the schema generated.
    """
    # Create a dataframe to use to build the schema
    columns = (
        json_normalize(data, separator="_", infer_schema_length=None)
        .lazy()
        .collect_schema()
        .names()
    )
    schema = {
        column: (Object if column in object_columns else String) for column in columns
    }

    return schema


def concatenate_to_string_lazyframe(
    objs: list[dict] | dict[Never, Never] | list[Never] | Iterator,
    object_columns: list[str],
    batch_size: int = 2000,
) -> LazyFrame:
    """
    Flattens JSON data. Returns a LazyFrame with columns of type `String`.
    """
    lf = LazyFrame()

    for data in chunked(objs, batch_size):
        schema = get_polars_schema(data=data, object_columns=object_columns)
        response_lf = (
            json_normalize(data, separator="_", schema=schema)
            .lazy()
            .with_columns(
                col(Object).map_elements(lambda x: str(x), return_dtype=String)
            )
        )
        lf = concat([lf, response_lf], how="diagonal")

    return lf

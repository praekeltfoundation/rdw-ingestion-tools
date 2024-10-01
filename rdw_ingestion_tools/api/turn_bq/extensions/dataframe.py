from collections.abc import Iterator

from pandas import DataFrame, concat, json_normalize


def concatenate(objs: list[dict] | dict | list | Iterator) -> DataFrame:
    """
    extend pandas concat to not only support dicts or lists of dicts, but
    also empty lists (which is often returned by the APIs).

    """
    try:
        df = concat([json_normalize(obj, sep="_") for obj in objs])
    except ValueError:
        df = DataFrame()

    return df

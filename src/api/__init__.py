import os


class MissingConfig(Exception):
    pass


def config_from_env(key: str) -> str:
    if not (value := os.environ.get(key, None)):
        raise MissingConfig(f"{key} not set in the global environment")
    return value

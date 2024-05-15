import os


class MissingConfig(Exception):
    """Raised if a required config environment variable is not set."""


def config_from_env(key: str) -> str:
    """Checks whether key exists in global environment and returns it if it
    does. Else it raises a MissingConfig Exception.

    """
    if not (value := os.environ.get(key, None)):
        raise MissingConfig(f"{key} not set in the global environment")
    return value

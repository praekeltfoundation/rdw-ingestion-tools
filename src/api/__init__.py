import os


class MissingConfig(Exception):
    """Raised if a required config environment variable is not set."""


def config_from_env(key: str) -> str:
    """Fetches a config value from the global environment, raising
    MissingConfig if it isn't there.

    """
    if not (value := os.environ.get(key, None)):
        raise MissingConfig(f"{key} not set in the global environment")
    return value

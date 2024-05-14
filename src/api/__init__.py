import os


class MissingConfig(Exception):
    """Exception to return if an env var is not found in the global
    environment.
    """


def config_from_env(key: str) -> str:
    """Checks whether key exists in global environment and returns it if it
    does. Else it returns a MissingConfig Exception.

    Args:
       key: The name of the env var to return. (str)

    Returns:
       str
    """
    if not (value := os.environ.get(key, None)):
        raise MissingConfig(f"{key} not set in the global environment")
    return value

import os

from boto3 import Session


class MissingConfig(Exception):
    """Raised if a required config environment variable is not set."""


def config_from_env(key: str) -> str:
    """Fetches a config value from the global environment, raising
    MissingConfig if it isn't there.

    """
    if not (value := os.environ.get(key, None)):
        raise MissingConfig(f"{key} not set in the global environment")
    return value


S3_KEY = config_from_env("S3_KEY")
S3_SECRET = config_from_env("S3_SECRET")


session: Session = Session(
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET,
    region_name="af-south-1",
)

from .main import pyS3 as pyS3

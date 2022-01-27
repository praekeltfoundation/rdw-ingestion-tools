import os

from boto3 import Session


class S3KeyMissingError(Exception):
    pass


try:
    S3_KEY = os.environ["S3_KEY"]
except KeyError:
    raise S3KeyMissingError(
        "Unable to locate S3_KEY in the global environment."
    )

try:
    S3_SECRET = os.environ["S3_SECRET"]
except KeyError:
    raise S3KeyMissingError(
        "Unable to locate S3_SECRET in the global environment."
    )


if not all([S3_KEY, S3_SECRET]):
    raise S3KeyMissingError(
        "Unable to locate one or both of S3_KEY and S3_SECRET in the global enviroment."
    )


class Session(Session):
    def __init__(self, key, secret):
        super().__init__(
            aws_access_key_id=key,
            aws_secret_access_key=secret,
            region_name="af-south-1",
        )


session = Session(key=S3_KEY, secret=S3_SECRET)

from .main import pyS3

from s3.s3.s3 import S3

from . import session


class pyS3:
    """A wrapper class for different s3 submodules."""

    s3 = S3(session)

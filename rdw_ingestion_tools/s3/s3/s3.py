from collections.abc import Iterator
from typing import Literal

import awswrangler as wr
from attrs import define
from boto3 import Session
from pandas import DataFrame


@define
class S3:
    """For simple S3 operations required by the ingestion pipeline."""

    _session: Session

    def is_empty(self, bucket: str, prefix: str) -> bool:
        """Check whether a prefix exists in a bucket."""
        response = self._session.client("s3").list_objects_v2(
            Bucket=bucket, Prefix=prefix
        )

        return "Contents" not in response

    def get_paginator(self, bucket: str, prefix: str) -> Iterator[dict]:
        """See aws reference for the paginator below.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/paginator/ListObjectsV2.html

        Creates an iterator that will paginate through responses from
        S3.Client.list_objects_v2()

        """
        paginator = self._session.client("s3").get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

        return pages

    def get_last_modified(self, bucket: str, prefix: str) -> str:
        """Get the latest modified time for files in a prefix."""
        times = []

        pages = self.get_paginator(bucket=bucket, prefix=prefix)

        for page in pages:
            for record in page["Contents"]:
                times.append(record["LastModified"])

        return max(times)

    def get_filenames(self, bucket: str, prefix: str) -> list[str]:
        """List filenames in a prefix."""
        pages = self.get_paginator(bucket=bucket, prefix=prefix)

        filenames = []

        for page in pages:
            for record in page["Contents"]:
                filenames.append(record["Key"])
        return filenames

    def read(self, path: str) -> DataFrame:
        """Read a parquet file from s3 into a python session."""
        return wr.s3.read_parquet(path, boto3_session=self._session)

    def read_csv(self, path: str) -> DataFrame:
        """Read a csv file from s3 into a python session."""
        return wr.s3.read_csv(path, boto3_session=self._session)

    def write(
        self,
        df: DataFrame,
        path: str | None = None,
        dataset: bool = True,
        dtype: dict[str, str] | None = None,
        mode: (Literal["append", "overwrite", "overwrite_partitions"] | None) = None,
    ) -> None:
        """Write a DataFrame to parquet in s3."""
        wr.s3.to_parquet(
            df=df,
            path=path,
            dataset=dataset,
            boto3_session=self._session,
            mode=mode,
            dtype=dtype,
        )

import awswrangler as wr


class S3:
    def __init__(self, session):
        self._session = session

    def is_empty(self, bucket, prefix):
        response = self._session.client("s3").list_objects_v2(
            Bucket=bucket, Prefix=prefix
        )

        return "Contents" not in response

    def get_paginator(self, bucket, prefix):
        paginator = self._session.client("s3").get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
        return pages

    def get_last_modified(self, bucket, prefix):
        times = []

        pages = self.get_paginator(bucket=bucket, prefix=prefix)

        for page in pages:
            for record in page["Contents"]:
                times.append(record["LastModified"])

        return max(times)

    def get_filenames(self, bucket, prefix):
        pages = self.get_paginator(bucket=bucket, prefix=prefix)

        filenames = []

        for page in pages:
            for record in page["Contents"]:
                filenames.append(record["Key"])
        return filenames

    def read(self, path):
        return wr.s3.read_parquet(path, boto3_session=self._session)

    def read_csv(self, path):
        return wr.s3.read_csv(path, boto3_session=self._session)

    def write(self, df, path, dataset=True, dtype=None, mode=None):
        wr.s3.to_parquet(
            df=df,
            path=path,
            dataset=dataset,
            boto3_session=self._session,
            mode=mode,
            dtype=dtype,
        )

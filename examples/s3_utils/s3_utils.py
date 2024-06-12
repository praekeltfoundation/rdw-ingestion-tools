import os

from s3 import pyS3

BUCKET = os.environ["BUCKET"]
PREFIX = os.environ["PREFIX"]

is_empty = pyS3.s3.is_empty(bucket=BUCKET, prefix=PREFIX)

print(f"Is prefix {PREFIX} empty: {is_empty}")

modified = pyS3.s3.get_last_modified(bucket=BUCKET, prefix=PREFIX)

print(f"Prefix {PREFIX} last modified: {modified}")

files = pyS3.s3.get_filenames(bucket=BUCKET, prefix=PREFIX)

print(f"Files: {files}")

state = pyS3.s3.read("s3://rdw-za/mnch/mnch-turn/contacts/state.parquet")

print(f"State: {state}")

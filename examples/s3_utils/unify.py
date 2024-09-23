"""
Usage example: pr python3 examples/s3_utils/unify.py --bucket 'rdw-za' --prefix 'contact-ndoh/momconnect-flow-results/flows/questions/'

"""

import argparse
import os

from pandas import concat
from s3 import pyS3
from tqdm import tqdm

command_line_parser = argparse.ArgumentParser()

command_line_parser.add_argument(
    "-p",
    "--prefix",
    type=str,
    help="The prefix of the file in AWS S3.",
    required=True,
)
command_line_parser.add_argument(
    "-b",
    "--bucket",
    type=str,
    help="The S3 bucket.",
    required=True,
)
command_line_parser.add_argument(
    "-t",
    "--test",
    type=str,
    help="Whether to run in test mode.",
    default="True",
    required=False,
)

command_line_args = command_line_parser.parse_args()

if __name__ == "__main__":
    files = pyS3.s3.get_filenames(
        command_line_args.bucket, command_line_args.prefix
    )

    dfs = []
    for file in tqdm(files):
        dfs.append(pyS3.s3.read(f"s3://{command_line_args.bucket}/{file}"))
    df = concat(dfs)
    if command_line_args.test == "True":
        print("Files successfully loaded into Python session.")
        print("Records:", len(df))
        print("Fields:", len(df.columns))
        print(
            "To be loaded to: ",
            "s3://",
            command_line_args.bucket,
            "/",
            command_line_args.prefix,
            sep="",
        )
    elif command_line_args.test == "False":
        pyS3.s3.write(
            concat(dfs).astype(str),
            "s3://{command_line_args.bucket}/{command_line_args.prefix}/",
        )
        print("Wrote unified dataset.")

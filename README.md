<h1 align="center">
  :octocat: rdw-ingestion-tools
</h1>

<div align="center">
  <p>
    <img src="https://github.com/praekeltfoundation/rdw-ingestion-tools/workflows/lint/badge.svg" width="120" />
    <img src="https://github.com/praekeltfoundation/rdw-ingestion-tools/workflows/release/badge.svg" width="145" />
    <img src="https://img.shields.io/badge/version-0.3.2-orange" width="112" />
    <img src="https://img.shields.io/badge/license-MIT-blue" width="100" />
  </p>
</div>


A DS team repository for shared data ingestion utilities. 

## usage

To interact with an API.

```
from api.flow_results import pyFlows

pyFlows.flows.get_ids()
```

To access some of the s3 utilities used in ingestion. 

```
import os
from s3 import pyS3

bucket=os.environ["BUCKET_NAME"]
prefix=os.environ["PREFIX"]

pyS3.s3.get_filenames(bucket=bucket, prefix=prefix)
```

## to-do

- Add tests - yes, I am a bad developer for not having any yet.
- Add release pipeline when tests are done.
- Write a decent README. 

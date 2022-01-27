
<div align="right">
  <p>
    <img src="https://github.com/praekeltfoundation/rdw-ingestion-tools/workflows/black-lint/badge.svg" width="120" />
    <img src="https://github.com/praekeltfoundation/rdw-ingestion-tools/workflows/isort-lint/badge.svg" width="120" />
  </p>
</div>
  
# rdw-ingestion-tools

A DS team repository for shared data ingestion utilities. 

## usage

To interact with an API.

```
from api import API

API.pyFlows.flows.get_ids()
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

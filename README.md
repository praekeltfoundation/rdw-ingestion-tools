<h1 align="center">
  :octocat: rdw-ingestion-tools
</h1>

<div align="center">
  <p>
    <img src="https://github.com/praekeltfoundation/rdw-ingestion-tools/workflows/lint/badge.svg" width="120" />
    <img src="https://github.com/praekeltfoundation/rdw-ingestion-tools/workflows/release/badge.svg" width="145" />
    <img src="https://img.shields.io/badge/version-1.0.4.dev0-orange" width="145" />
    <img src="https://img.shields.io/badge/license-MIT-blue" width="100" />
  </p>
</div>


A DS team repository for shared data ingestion utilities.

## setup

### 1. Ensure the necessary global environment variables are set in your Python environment.

- For aaq:

```
AAQ_API_KEY="<secret>"
AAQ_API_BASE_URL="<url>"

```

- For content_repo:

```
CONTENT_REPO_API_KEY="<secret>"
CONTENT_REPO_BASE_URL="<url>"

```

- For flow_results:

```
FLOW_RESULTS_API_KEY="<secret>"
FLOW_RESULTS_API_BASE_URL="<url>"

```

- For rapidpro:

```
RAPIDPRO_API_KEY="<secret>"
RAPIDPRO_API_BASE_URL="<url>"

```
- For survey:

```
SURVEY_API_KEY="<secret>"
SURVEY_API_BASE_URL="<url>"

```

- For turn: (Original Data Export API)

```
TURN_API_KEY="<secret>"
TURN_API_BASE_URL="<url>"

```

For the turn_bq API: (New Addition)

```
TURN_BQ_API_KEY="<secret>"
TURN_BQ_API_BASE_URL="<url>"

```

If you want to use the s3 utilities (that allow you to read and write specific parquet files amongst other things), the following variables should be set:

```
S3_KEY="<key>"
S3_SECRET="<secret>"

```

### 2. Install the `rdw-ingestion-tools` package

There are 2 ways of doing this.

- Versioned install from github:

`rdw-ingestion-tools` is public!

```
pip3 install git+https://github.com/praekeltfoundation/rdw-ingestion-tools@v1.0.2
```

- From clone (with [uv](https://docs.astral.sh/uv/)). This is recommended:

```
git clone git@github.com:praekeltfoundation/rdw-ingestion-tools.git

uv sync

```

## usage

For more examples on how to interact with particular API endpoints, see the `examples` file. These
contain examples for each supported third party service and the endpoint associated with each.

For instance, to get flows from the Flow Results Specification API, the example is as follows:

```
from api.flow_results import pyFlows

flows = pyFlows.flows.get_flows()

print(flows.keys())
```

To access some of the s3 utilities used in ingestion.

```
import os
from s3 import pyS3

bucket=os.environ["BUCKET_NAME"]
prefix=os.environ["PREFIX"]

pyS3.s3.get_filenames(bucket=bucket, prefix=prefix)
```

### Running an example locally
1. `uv sync`
2. `uv run --env-file .env examples/{path}` e.g. `uv run --env-file .env examples/turn_bq/cards.py`

## to-do

- Add tests - yes, I am a bad developer for not having any yet.

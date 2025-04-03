#!/bin/sh

# This is a function to better handle paths that may contains whitespace.
fmt() {
    ruff format "$@"
}

fmt rdw_ingestion_tools/ examples/ tests/

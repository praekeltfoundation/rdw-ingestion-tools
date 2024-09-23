#!/bin/sh

# This is a function to better handle paths that may contains whitespace.
fmt() {
    ruff check --select=I --fix "$@"
    black "$@"
}

fmt rdw_ingestion_tools/ examples/

#!/bin/bash
set -ex

# Convenience workspace directory for later use
WORKSPACE_DIR=$(pwd)

# Change some Poetry settings to better deal with working in a container
poetry config cache-dir ${WORKSPACE_DIR}/.cache

# Now install all dependencies
poetry install
poetry run pre-commit install -t pre-commit -t commit-msg

echo "Done!"

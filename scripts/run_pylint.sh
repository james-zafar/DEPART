#!/bin/bash

set -e

cd "$(dirname "$0")/.." || exit

if ! python -m pylint --fail-under=9.0  ./app; then
    exit 1
fi

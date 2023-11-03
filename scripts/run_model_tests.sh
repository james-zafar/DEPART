#!/bin/bash

cd "$(dirname "$0")/.." || exit

python -m unittest discover -s "$(pwd)/tests/model" -p 'test*'

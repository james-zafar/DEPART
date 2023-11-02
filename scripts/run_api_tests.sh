#!/bin/bash

cd "$(dirname "$0")/.." || exit

python -W ignore -m unittest discover -s "$(pwd)/tests/api" -p 'test*'

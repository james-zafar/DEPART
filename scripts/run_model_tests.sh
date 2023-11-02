#!/bin/bash

cd "$(dirname "$0")/.." || exit

python -m unittest tests.model.test_model

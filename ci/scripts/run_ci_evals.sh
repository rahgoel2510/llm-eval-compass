#!/bin/bash
set -e
pip install -r requirements.txt
python pipelines/regression_pipeline.py

#!/bin/bash

> nohup.out
echo "Opening environment"
source env/bin/activate
python3 WebAnalyzer.py

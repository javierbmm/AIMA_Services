#!/bin/bash
sudo chmod u+x Executer.sh

echo "Opening environment"
source ../bin/activate
python3 WebAnalyzer.py

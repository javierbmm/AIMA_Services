#!/bin/bash
chmod +x Executer.sh

echo "Opening environment"
cd .. 
source bin/activate
cd WebAnalyzer/Linux
python3 WebAnalyzer.py

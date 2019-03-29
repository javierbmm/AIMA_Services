@echo off
cmd /k "cd .. & py -m virtualenv . & /d .\Scripts\activate & cd /d .\WebAnalyzer & pip install -r requirements.txt & py WebAnalyzer.py"
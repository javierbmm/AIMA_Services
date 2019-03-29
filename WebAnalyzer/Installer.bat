@echo off
cmd /k "cd .. & py -m virtualenv . & .\Scripts\activate & cd /d .\WebAnalyzer & pip install -r requirements.txt & exit"

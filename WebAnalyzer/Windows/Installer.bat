@echo off
cmd /k "cd .. & py -m virtualenv . & .\Scripts\activate & cd /d .\Windows & pip install -r requirements.txt & exit"

#!/bin/bash
chmod u+x Installer.sh

echo "Setting virtual environment"
cd .. 
py -m virtualenv .
source bin/activate
cd WebAnalyzer/Linux
echo "Installing requirements"
pip install -r requirements.txt
echo "Installation successfully done"

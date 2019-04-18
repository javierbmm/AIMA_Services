#!/bin/bash
sudo chmod u+x Installer.sh

echo "Setting virtual environment"
cd .. 
virtualenv --python python3 .
source bin/activate
cd WebAnalyzer/Linux
echo "Installing requirements"
pip install -r requirements.txt
echo "Installation successfully done"

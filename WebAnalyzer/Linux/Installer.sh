#!/bin/bash
sudo chmod u+x Installer.sh

echo "Setting virtual environment"
cd .. 
virtualenv --python python3 .
nohup sleep 10 &
source bin/activate
cd WebAnalyzer/Linux
echo "Installing requirements"
pip install -r requirements.txt
nohup sleep 10 &
echo "Installation successfully done"

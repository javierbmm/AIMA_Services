#!/bin/bash
sudo chmod u+x Installer.sh

echo "Setting virtual environment"
virtualenv --python python3 .
nohup sleep 10 &
source ../bin/activate
echo "Installing requirements"
pip install -r requirements.txt
echo "Installation successfully done"

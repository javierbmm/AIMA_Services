#!/bin/bash
sudo chmod u+x Installer.sh

echo "Installing Chrome"
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable

echo "Setting virtual environment"
virtualenv --python python3 .
nohup sleep 10 &
source ../bin/activate
echo "Installing requirements"
pip install -r requirements.txt
echo "Installation successfully done"

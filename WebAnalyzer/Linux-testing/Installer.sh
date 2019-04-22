#!/bin/bash
sudo chmod u+x Installer.sh

echo "Installing Python, pip and virtualenv"
sudo apt update
sudo apt install python python-dev python3 python3-dev
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
pip install --upgrade virtualenv

echo "Installing Chrome"
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
sudo echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable

echo "Setting chromedriver"
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver

echo "Setting virtual environment"
virtualenv --python python3 env
nohup sleep 10 &
source env/bin/activate
echo "Installing requirements"
pip install -r requirements.txt
echo "Installation successfully done"

chmod u+x Executer.sh
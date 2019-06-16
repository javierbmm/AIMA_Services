#!/bin/bash

echo "Updating..."
pkill chrome
pkill chromedriver
pkill python3
pkill nohup
>nohup.out
git pull
echo "Done!"
#!/bin/bash
curl -O https://github.com/littleblack111/pbackup/archive/refs/heads/main.zip
unzip main.zip || zip -d main.zip
pushd main
pip install -r requirements.txt || echo no requirements.txt found
sudo install main.py /usr/bin/bbackup
sudo install stdlib.py /usr/bin

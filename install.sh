#!/bin/bash
curl -O https://codeload.github.com/littleblack111/pbackup/zip/refs/heads/main
unzip main || zip -d main
pushd pbackup-main
pip install -r requirements.txt || echo no requirements.txt found
sudo install main.py /usr/bin/bbackup
sudo install stdlib.py /usr/bin
popd
pbackup

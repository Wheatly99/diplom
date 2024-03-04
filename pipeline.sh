#!/bin/bash
rm -rf git_repo
mkdir git_repo

git clone $1 git_repo
pip3 install -r git_repo/lab1/requirements.txt

python3 main.py $2

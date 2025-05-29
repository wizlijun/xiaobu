#!/bin/bash

python3 -m venv venv
source venv/bin/activate

python genindex.py ~/git/xiaobu/ai https://www.xiaobu.net/ai/

export http_proxy=http://127.0.0.1:1087;export https_proxy=http://127.0.0.1:1087;

git add .

git commit -m "$(date '+%Y-%m-%d %H:%M:%S')"

git push

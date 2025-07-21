#!/bin/bash

python3 -m venv venv
source venv/bin/activate

python3 genindex.py ~/git/xiaobu/ai https://www.laobu.net/ai/
python3 gensitemap.py -u https://www.laobu.net

export http_proxy=http://127.0.0.1:1087;export https_proxy=http://127.0.0.1:1087;

git add .

git commit -m "$(date '+%Y-%m-%d %H:%M:%S')"

git push

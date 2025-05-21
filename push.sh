#!/bin/bash

python3 genindex.py ~/git/xiaobu/ai https://www.xiaobu.net/ai/

git add .

git commit -m "$(date '+%Y-%m-%d %H:%M:%S')"

git push
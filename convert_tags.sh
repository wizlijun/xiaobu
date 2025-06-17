#!/bin/bash

# 查找所有的 meta.yaml 文件
find . -name "meta.yaml" -type f | while read file; do
    # 使用 sed 将 tags 部分的内容转换为小写
    sed -i '' -E '/^tags:/,/^[a-z]/ { /^-/ s/.*/\L&/ }' "$file"
done 
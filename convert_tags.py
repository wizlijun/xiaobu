#!/usr/bin/env python3
import os
import yaml
import glob

def convert_tags_to_lowercase(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 YAML
        data = yaml.safe_load(content)
        
        # 如果存在 tags，将其转换为小写
        if 'tags' in data and isinstance(data['tags'], list):
            data['tags'] = [tag.lower() for tag in data['tags']]
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False)
            print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def main():
    # 查找所有的 meta.yaml 文件
    meta_files = glob.glob('**/meta.yaml', recursive=True)
    
    for file_path in meta_files:
        convert_tags_to_lowercase(file_path)

if __name__ == '__main__':
    main() 
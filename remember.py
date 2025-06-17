#!/bin/env python3

import os
import sys
import shutil
import json
import hashlib

def load_map(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_map(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def calculate_file_hash(file_path, hash_algorithm='md5'):
    """Calculate the hash of a file."""
    hash_func = hashlib.new(hash_algorithm)

    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)

    return hash_func.hexdigest()

def compare_files(file1, file2):
    """Compare the hashes of two files."""
    hash1 = calculate_file_hash(file1)
    hash2 = calculate_file_hash(file2)

    return hash1 == hash2

directory_path = "./history"
os.makedirs(directory_path, exist_ok=True)

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} <file>")
    exit(1)

target_file = sys.argv[1]

map_path = f"{directory_path}/latest.json"
m = load_map(map_path)

if target_file not in m:
    m[target_file] = 0
file_count = m[target_file] + 1

file_path = f"{directory_path}/{file_count:03}_{target_file}"
source_path = f"./{target_file}"

latest_path = f"{directory_path}/{m[target_file]:03}_{target_file}"
if os.path.exists(latest_path) and compare_files(latest_path, source_path):
    print("Nothing to do")
    exit(0)

shutil.copy(source_path, file_path)

m[target_file] = file_count
save_map(map_path, m)

print(f"{source_path} -> {file_path}")
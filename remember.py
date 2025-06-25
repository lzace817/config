#!/bin/env python3

import os
import sys
import shutil
import json
import hashlib
import difflib

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

def path_format(directory, n, name):
    return f"{directory}/{n:03}_{name}"


def write_patch(file1, file2, sink):
    """Write patch file1 and file2 to sink"""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        # Read the contents of the files
        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

    # Create a unified diff
    diff = difflib.unified_diff(
        f1_lines, f2_lines,
        fromfile=file1,
        tofile=file2,
        lineterm=''
    )

    # Write the diff to a patch file
    sink.write("``` patch\n")
    sink.writelines(diff)
    sink.write("```\n\n")

def create_diff_md():
    target_file = sys.argv[2]
    n = m[target_file]
    if n > 1:
        with open(f"diffs-{target_file}.md", 'w') as diffmd:
            previous_file = path_format(directory_path, 1, target_file)
            for i in range(2, n + 1):
                current_file = path_format(directory_path, i, target_file)
                assert(os.path.isfile(previous_file))
                write_patch(previous_file, current_file, diffmd)
                previous_file = current_file
    else:
        print("not enough files to diff")

directory_path = "./history"
os.makedirs(directory_path, exist_ok=True)

if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} add <file>", file=sys.stderr)
    print(f"       {sys.argv[0]} ls", file=sys.stderr)
    exit(1)

map_path = f"{directory_path}/latest.json"
m = load_map(map_path)

command = sys.argv[1]
if command == 'add':
    if len(sys.argv) < 3:
        print(f"{sys.argv[0]}: Missing file", file=sys.stderr)
        print(f"usage: {sys.argv[0]} add <file>", file=sys.stderr)
        exit(1)
    target_file = sys.argv[2]

    if target_file not in m:
        m[target_file] = 0
    file_count = m[target_file] + 1

    file_path = path_format(directory_path, file_count, target_file)
    source_path = f"./{target_file}"

    latest_path = path_format(directory_path, m[target_file], target_file)
    if os.path.exists(latest_path) and compare_files(latest_path, source_path):
        print("Nothing to do")
        exit(0)

    shutil.copy(source_path, file_path)

    m[target_file] = file_count
    save_map(map_path, m)

    print(f"{source_path} -> {file_path}")

elif command == 'ls':
    for target_file in m:
        latest_path = path_format(directory_path, m[target_file], target_file)
        print(latest_path)
elif command == 'patches':
    create_diff_md()
else:
    print(f"unkown command `{command}`")

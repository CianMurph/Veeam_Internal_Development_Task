import os
import hashlib

def scan_source(path):
    state = {}
    for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    hash = hashlib.md5(f.read()).hexdigest()
                state[file_path] = hash
    return state
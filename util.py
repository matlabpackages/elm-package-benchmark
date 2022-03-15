import json
import os

def read_json(file):
    with open(file, 'r') as f:
        obj = json.load(f)
    return obj

def write_json(file, obj, **kwargs):
    dir = os.path.dirname(file)
    if not os.path.isdir(dir):
        os.makedirs(dir)
    with open(file, 'w') as f:
        json.dump(obj, f, **kwargs)

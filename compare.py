# Compare Rust elm-solve-deps result (from result.yaml) with Python mixology result (from result.json)
from util import write_json
from yaml import load, Loader

file = 'result.yaml'
out_file = './result_rust.json'

with open(file, 'r') as f:
    data = load(f, Loader=Loader)
del data['stats']
del data['failed']
d = {}
for k in data:
    d[k.lower()] = data[k]

write_json(out_file, d, sort_keys=True, indent=2)

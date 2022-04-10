import toml
import os

def main():
    source = 'General'
    target = 'graph-julia.json'
    g = read_graph(source)

def read_graph(source_dir):
    reg_file = os.path.join(source_dir, 'Registry.toml')
    reg_data = toml.load(reg_file)
    uuid_to_name = {}
    name_to_uuid = {}
    graph = {}
    for uuid, info in reg_data['packages']:
        name = info['name']
        path = info['path']
        uuid_to_name[uuid] = name
        name_to_uuid[name] = uuid
        p = os.path.join(source_dir, path)
        versions = toml.load(os.path.join(p, 'Versions.toml'))
        deps = toml.load(os.path.join(p, 'Deps.toml'))
        compat = toml.load(os.path.join(p, 'Compat.toml'))
        # TODO
    return None

if __name__ == '__main__':
    main()

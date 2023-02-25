from util import write_json, read_json

def main():
    input_file = 'graph.json'
    output_file = './elm-packages.json'

    graph = read_json(input_file)
    packages = {}

    for name, versions in graph.items():
        packages[name] = {}
        for version, dependencies in versions.items():
            packages[name][version] = {}
            for dependency, constraint in dependencies.items():
                packages[name][version][dependency] = version_spec(constraint)

    write_json(output_file, packages, indent=2, sort_keys=True)


def version_spec(constraint):
    if ' <= v < ' in constraint:
        lower, upper = constraint.split(' <= v < ')
        return f'{lower} - {prev_version(upper)}'
    elif ' <= v <= ' in constraint:
        lower, upper = constraint.split(' <= v <= ')
        return f'{lower} - {upper}'
    else:
        raise ValueError(constraint)

def prev_version(ver):
    major, minor, patch = [int(v) for v in ver.split('.')]
    if patch != 0:
        p = f'{major}.{minor}.{patch-1}'
    elif minor != 0:
        p = f'{major}.{minor-1}.*';
    elif major != 0:
        p = f'{major-1}.*.*';
    else:
        ValueError('0.0.0 has no previous version')
    return p


if __name__ == '__main__':
    main()

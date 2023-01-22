import json
from use_mixology import PackageSource, VersionSolver, print_solution

# Run examples from
# https://github.com/dart-lang/pub/blob/master/doc/solver.md

def main():
    run_example('pubgrub_examples/no-conflicts.json')
    run_example('pubgrub_examples/avoid-conflict.json')
    run_example('pubgrub_examples/conflict-resolution.json')

def run_example(file):
    source = read_example(file)
    solver = VersionSolver(source)
    result = solver.solve()
    print(file)
    print_solution(solver, result)

def read_example(file):
    data = read_json(file)
    source = PackageSource()

    for name, spec in data['root'].items():
        source.root_dep(name, parse_constraint(spec))

    for pkg, versions in data['packages'].items():
        for ver, deps in versions.items():
            source.add(pkg, ver, deps=parse_constraints(deps))

    return source

def parse_constraint(spec):
    # convert spec from format '3.0.0 - 4.*.*' to '>=3.0.0 <5.0.0'
    if spec == '*':
        return spec
    lower, upper = spec.split(' - ')
    if upper == '*.*.*':
        up = ''
    elif '*' in upper:
        up = f' <{next_version(upper)}'
    else:
        up = f' <= {upper}'
    constraint = f'>={lower}{up}'
    return constraint

def parse_constraints(deps):
    d = {}
    for name, spec in deps.items():
        d[name] = parse_constraint(spec)
    return d

def next_version(ver):
    major, minor, patch = ver.split('.')
    if ver.count('*', 2): 
        return version(int(major) + 1, 0, 0)
    elif ver.count('*', 1):
        return version(int(major), int(minor) + 1, 0)
    else:
        return version(int(major), int(minor), int(patch) + 1)

def version(major, minor, patch):
    return f'{major}.{minor}.{patch}'

def read_json(file):
    with open(file, 'r') as f:
        content = json.load(f)
    return content

if __name__ == '__main__':
    main()

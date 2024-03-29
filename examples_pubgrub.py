import json
from use_mixology import PackageSource, VersionSolver, print_solution

# Run examples from
# https://github.com/dart-lang/pub/blob/master/doc/solver.md

def main():
    run_example('pubgrub_examples/no-conflicts.json')
    run_example('pubgrub_examples/avoid-conflict.json')
    run_example('pubgrub_examples/conflict-resolution.json')
    run_example('pubgrub_examples/partial-satisfier.json')
    run_example('pubgrub_examples/error-linear.json')
    run_example('pubgrub_examples/error-branching.json')

def run_example(file):
    source = read_example(file)
    solver = VersionSolver(source)
    print(file)
    try:
        result = solver.solve()
        print_solution(solver, result)
    except Exception as e:
        print('Failure:')
        print(str(e))
    print('-' * 80)

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
    c = ver.count('*')
    if c == 2: 
        return version(int(major) + 1, 0, 0)
    elif c == 1:
        return version(int(major), int(minor) + 1, 0)
    elif c == 0:
        return version(int(major), int(minor), int(patch) + 1)
    else:
        raise ValueError(f'next version of {ver} is not valid')

def version(major, minor, patch):
    return f'{major}.{minor}.{patch}'

def read_json(file):
    with open(file, 'r') as f:
        content = json.load(f)
    return content

if __name__ == '__main__':
    main()

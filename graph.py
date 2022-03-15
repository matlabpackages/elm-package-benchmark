from util import read_json
from download import get_missing_packages

def main():
    g = read_json('graph.json')
    missing = get_missing_packages(g)
    for m in missing:
        print(m)
    all_deps = get_all_deps(g)
    for vers in all_deps:
        print(len(vers), vers)

def get_all_deps(graph):
    all_deps = []
    for package, versions in graph.items():
        for version, deps in versions.items():
            for dep, vers in deps.items():
                if dep not in graph:
                    raise ValueError(f'missing: {dep}')
                all_deps.append(vers)
    return all_deps

main()

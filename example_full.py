import time
from use_mixology import VersionSolver
from elm_util import create_full_package_source
from util import read_json, write_json
from mixology.failure import SolverFailure

# Elm package graph
start = time.process_time()
g = read_json('graph.json')
start = time.process_time()
source = create_full_package_source(g)
print('Create full source: ', time.process_time() - start, 'seconds')

# Set root package
packages = [
    'EngageSoftware/elm-engage-common',
    'Gizra/elm-fetch',
]
packages = g.keys()
start_solve = time.process_time()
n = len(packages)
n_fail = 0
overall_result = {}
for i, pkg in enumerate(packages):
    print(f'{i+1}/{n}: {pkg}')
    overall_result[pkg] = {}
    for ver in g[pkg]:
        source._root_dependencies = []  # reset
        source.root_dep(pkg, ver)
        solver = VersionSolver(source)
        try:
            result = solver.solve()
            if solver.is_solved():
                dec = {}
                for dec_pkg, dec_ver in result.decisions.items():
                    if isinstance(dec_pkg, str):
                        dec[dec_pkg] = str(dec_ver)
                overall_result[pkg][ver] = dec
            else:
                n_fail += 1
        except SolverFailure:
            n_fail += 1
write_json('./result.json', overall_result, indent=2, sort_keys=True)

print('Total solving time: ', time.process_time() - start_solve, 'seconds')
print(f'{n_fail} package versions failed')

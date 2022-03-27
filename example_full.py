import imp
import time
from use_mixology import VersionSolver
from elm_util import create_full_package_source
from util import read_json
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
for i, pkg in enumerate(packages):
    print(f'{i+1}/{n}: {pkg}')
    for ver in g[pkg]:
        source._root_dependencies = []  # reset
        source.root_dep(pkg, ver)

        #start = time.process_time()
        solver = VersionSolver(source)
        try:
            result = solver.solve()
            if not solver.is_solved():
                n_fail += 1
        except SolverFailure:
            n_fail += 1

print('Total solving time: ', time.process_time() - start_solve, 'seconds')
print(f'{n_fail} package versions failed')

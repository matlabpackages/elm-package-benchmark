import time
from use_mixology import VersionSolver, print_solution
from elm_util import create_package_source, create_full_package_source

# Example
from util import read_json

# Elm package graph
start = time.process_time()
g = read_json('graph.json')
print('Reading graph: ', time.process_time() - start, 'seconds')

# Package source for specific root package
pkg = 'EngageSoftware/elm-engage-common'
ver = '3.1.0'
#pkg = 'Gizra/elm-fetch'
#ver = '1.0.0'
start = time.process_time()
source = create_package_source(g, pkg, ver)
print('Create source: ', time.process_time() - start, 'seconds')

# Solve
start = time.process_time()
solver = VersionSolver(source)
print('Create solver: ', time.process_time() - start, 'seconds')

start = time.process_time()
result = solver.solve()
print('Solving: ', time.process_time() - start, 'seconds')
print_solution(solver, result)

# Full universe
start = time.process_time()
source = create_full_package_source(g)
print('Create full source: ', time.process_time() - start, 'seconds')

start = time.process_time()
source.root_dep(pkg, ver)
print('Add root: ', time.process_time() - start, 'seconds')

start = time.process_time()
solver = VersionSolver(source)
print('Create solver: ', time.process_time() - start, 'seconds')

start = time.process_time()
result = solver.solve()
print('Solving: ', time.process_time() - start, 'seconds')
print_solution(solver, result)

from use_mixology import PackageSource, VersionSolver, print_solution

# Simple example

source = PackageSource()

source.root_dep("a", "1.0.0")
source.root_dep("b", "1.0.0")

source.add("a", "1.0.0", deps={"shared": ">=2.0.0 <4.0.0"})
source.add("b", "1.0.0", deps={"shared": ">=3.0.0 <5.0.0"})
#source.add("b", "1.0.0", deps={"shared": ">=1.0.0 <2.0.0"})
source.add("shared", "1.0.0")
source.add("shared", "1.5.0")
source.add("shared", "2.0.0")
source.add("shared", "3.0.0")
source.add("shared", "3.6.9")
source.add("shared", "4.0.0")
source.add("shared", "5.0.0")

# Solve

solver = VersionSolver(source)
result = solver.solve()
print_solution(solver, result)

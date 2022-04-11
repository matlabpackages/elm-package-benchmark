import Solver: julia_package, julia_registry, resolve_julia_deps, solve_julia
using Pkg

deps = [julia_package("ModelingToolkit", "8.5.4")]
registries = [julia_registry("General")]
@time solution = resolve_julia_deps(deps, registries)

# solve all package versions
solutions = solve_julia("General")

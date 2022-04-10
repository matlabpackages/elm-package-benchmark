import Solver: julia_package, julia_registry, resolve_julia_deps

deps = [julia_package("ModelingToolkit", "8.5.4")]
registries = [julia_registry("General")]
@time solution = resolve_julia_deps(deps, registries)

import Solver: julia_package, julia_registry, resolve_julia_deps, package_versions
using Pkg

deps = [julia_package("ModelingToolkit", "8.5.4")]
registries = [julia_registry("General")]
@time solution = resolve_julia_deps(deps, registries)

reg = registries[1]
pv = package_versions(reg)

const PackageSpec = Pkg.PackageSpec

# Solve every version of every package
solutions = Dict{String,Dict{String,Vector{PackageSpec}}}()
for (pkg, vers) in pv
    solutions[pkg] = Dict()
    for ver in vers
        println("$pkg $ver")
        deps = [julia_package(pkg, ver)]
        try
            @time solution = resolve_julia_deps(deps, registries)
        catch err
            solution = []
        end
        solutions[pkg][ver] = solution
    end
end

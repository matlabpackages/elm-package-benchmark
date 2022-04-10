module Solver

using UUIDs
using Pkg
using Pkg.Resolve
using JSON

const Fixed = Pkg.Resolve.Fixed
const Graph = Pkg.Resolve.Graph
const VersionSpec = Pkg.Versions.VersionSpec
const VersionRange = Pkg.Versions.VersionRange
const VersionBound = Pkg.Versions.VersionBound

function graph(compat, uuid_to_name, reqs)
    fixed = Dict{UUID,Fixed}()
    verbose = false
    julia_version = VERSION
    g = Graph(compat, uuid_to_name, reqs, fixed, verbose, julia_version)
    return g
end

function use_names(sol, uuid_to_name)
    n = Dict{String, String}()
    for (u, v) in sol
        n[uuid_to_name[u]] = string(v)
    end
    return n
end

function range(string)
    parts = split(string, " - ")
    lo = parts[1]
    hi = parts[2]
    lower = VersionBound(VersionNumber(lo))
    wildcards = length(findall("*", hi))
    n = 3 - wildcards
    vers = split(hi, ".")
    if n == 0
        higher = VersionBound()
    elseif n == 1
        higher = VersionBound(parse(Int, vers[1]))
    elseif n == 2
        higher = VersionBound(parse(Int, vers[1]), parse(Int, vers[2]))
    elseif n == 3
        higher = VersionBound(parse(Int, vers[1]), parse(Int, vers[2]), parse(Int, vers[3]))
    end
    return VersionRange(lower, higher)
end

function version_spec(string)
    ranges = split(string, ", ")
    return VersionSpec([range(r) for r in ranges])
end

function solve(g)
    sol = resolve(g)
    use_names(sol, g.data.uuid_to_name)
end

function read_elm_graph(file)
    data = JSON.parsefile(file)
    uuid_to_name = Dict{UUID,String}()
    name_to_uuid = Dict{String,UUID}()
    for (pkg_name, _) in data
        u = UUIDs.uuid4()
        uuid_to_name[u] = pkg_name
        name_to_uuid[pkg_name] = u
    end
    compat = Dict{UUID,Dict{VersionNumber,Dict{UUID,VersionSpec}}}()
    for (pkg_name, vers) in data
        u = name_to_uuid[pkg_name]
        compat[u] = Dict()
        for (ver, specs) in vers
            v = VersionNumber(ver)
            compat[u][v] = convert_elm_specs(specs, name_to_uuid)
        end
    end
    return compat, uuid_to_name
end

function convert_elm_specs(specs, name_to_uuid)
    s = Dict{UUID,VersionSpec}()
    for (pkg_name, ver_spec) in specs
        u = name_to_uuid[pkg_name]
        s[u] = elm_version_constraint_to_spec(ver_spec)
    end
    return s
end

function elm_version_constraint_to_spec(ver_spec)
    if occursin(" <= v <= ", ver_spec)
        lo, hi = split(ver_spec, " <= v <= ")
    elseif occursin(" <= v < ", ver_spec)
        lo, hi_bound = split(ver_spec, " <= v < ")
        # 1.2.3 -> 1.2.2
        # 1.2.0 -> 1.1.*
        # 1.0.0 -> 0.*.*
        major, minor, patch = [parse(Int, item) for item in split(hi_bound, ".")]
        if patch > 0
            hi = "$(major).$(minor).$(patch-1)"
        elseif minor > 0  # patch == 0
            hi = "$(major).$(minor-1).*"
        elseif major > 0 # minor == 0 and patch == 0
            hi = "$(major-1).*.*"
        else
            error("unknown higher version: '$hi_bound'")
        end
    else
        error("unknown format: '$ver_spec'")
    end
    return version_spec("$lo - $hi")
end

function reduce_graph(compat, target_uuids)
    c = Dict{UUID,Dict{VersionNumber,Dict{UUID,VersionSpec}}}()
    for u in target_uuids
        add_package_recursive!(c, compat, u)
    end
    return c
end

function add_package_recursive!(c, compat, uuid)
    if !(uuid in keys(c))
        c[uuid] = compat[uuid]
        dep_uuids = []
        for (ver, specs) in compat[uuid]
            for (dep_uuid, _) in specs
                if !(dep_uuid in dep_uuids)
                    push!(dep_uuids, dep_uuid)
                end
            end
        end
        for dep_uuid in dep_uuids
            add_package_recursive!(c, compat, dep_uuid)
        end
    end
end

function solve_elm(compat, uuid_to_name)
    # Solve every version of every package
    solutions = Dict{String,Dict{String,Dict{String,String}}}()
    for (u, vers) in compat
        name = uuid_to_name[u]
        println("solving $name")
        solutions[name] = Dict()
        compat_reduced = Solver.reduce_graph(compat, [u])
        for (ver, _) in vers
            v = string(ver)
            reqs = Dict(u => Solver.version_spec("$v - $v"))
            g = Solver.graph(compat_reduced, uuid_to_name, reqs)
            sol = Dict()
            try
                sol = Solver.solve(g)
            catch err
            end
            solutions[name][v] = sol
        end
    end
    return solutions
end

function julia_package(name, version)
    return PackageSpec(name=name, version=Pkg.Versions.VersionSpec(version))
end

function julia_registry(path)
    return Pkg.Registry.RegistryInstance(path)
end

function resolve_julia_deps(deps, registries)
    preserve = Pkg.Types.PRESERVE_TIERED
    temp_env = Pkg.Types.EnvCache(Pkg.Types.projectfile_path("."))
    temp_io = devnull

    pkgs = deepcopy(deps)
    for pkg in pkgs
        pkg.version = Pkg.Versions.VersionSpec(pkg.version)
    end
    Pkg.Types.registry_resolve!(registries, pkgs)
    julia_version = VERSION
    pkgs, _ = Pkg.Operations._resolve(temp_io, temp_env, registries, pkgs, preserve, julia_version)
    return pkgs
end

end

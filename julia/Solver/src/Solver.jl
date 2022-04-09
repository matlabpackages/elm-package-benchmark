module Solver

using UUIDs
using Pkg
using Pkg.Resolve

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
    n = Dict{String, VersionNumber}()
    for (u, v) in sol
        n[uuid_to_name[u]] = v
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

end

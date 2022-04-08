using Pkg
using Pkg.Resolve
using UUIDs

const Fixed = Pkg.Resolve.Fixed
const Graph = Pkg.Resolve.Graph
const VersionSpec = Pkg.Versions.VersionSpec
const VersionRange = Pkg.Versions.VersionRange
const VersionBound = Pkg.Versions.VersionBound

a_uuid = UUIDs.uuid4()
b_uuid = UUIDs.uuid4()
shared_uuid = UUIDs.uuid4()

compat = Dict{UUID,Dict{VersionNumber,Dict{UUID,VersionSpec}}}(
    a_uuid => Dict(
        VersionNumber("1.0.0") => Dict(
            shared_uuid => version_spec("2.0.0 - 3.*.*")
        )
    ),
    b_uuid => Dict(
        VersionNumber("1.0.0") => Dict(
            shared_uuid => version_spec("3.0.0 - 5.*.*")
        )
    ),
    shared_uuid => Dict(
        VersionNumber("1.0.0") => Dict(),
        VersionNumber("1.5.0") => Dict(),
        VersionNumber("2.0.0") => Dict(),
        VersionNumber("3.0.0") => Dict(),
        VersionNumber("3.6.9") => Dict(),
        VersionNumber("4.0.0") => Dict(),
        VersionNumber("5.0.0") => Dict()
    )
)
uuid_to_name = Dict{UUID,String}(
    a_uuid => "a",
    b_uuid => "b",
    shared_uuid => "shared",
)
reqs = Dict{UUID,VersionSpec}(
    a_uuid => version_spec("1.0.0 - 1.0.0"),
    b_uuid => version_spec("1.0.0 - 1.0.0")
)
fixed = Dict{UUID,Fixed}()
verbose = false
julia_version = VERSION

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

function use_names(sol, uuid_to_name)
    n = Dict{String, VersionNumber}()
    for (u, v) in sol
        n[uuid_to_name[u]] = v
    end
    return n
end

spec = version_spec("1.1.0 - 2.0.0, 5.6.7 - 8.*.*")

g = Graph(compat, uuid_to_name, reqs, fixed, verbose, julia_version)

@time sol = resolve(g)

use_names(sol, uuid_to_name)

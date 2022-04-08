using UUIDs
using Pkg.Resolve

include("solver.jl")

version_spec = PackageSolver.version_spec
VersionSpec = PackageSolver.VersionSpec

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

spec = version_spec("1.1.0 - 2.0.0, 5.6.7 - 8.*.*")

g = PackageSolver.graph(compat, uuid_to_name, reqs)

@time sol = resolve(g)

PackageSolver.use_names(sol, uuid_to_name)

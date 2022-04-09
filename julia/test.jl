using Solver

# Read graph
compat, uuid_to_name = Solver.read_elm_graph("graph.json")

# Solve every version of every package
solutions = Dict{String,Dict{String,Dict{String,String}}}()
for (u, vers) in compat
    name = uuid_to_name[u]
    println("solving $name")
    solutions[name] = Dict()
    for (ver, _) in vers
        v = string(ver)
        reqs = Dict(u => Solver.version_spec("$v - $v"))
        g = Solver.graph(compat, uuid_to_name, reqs)
        sol = Dict()
        try
            sol = Solver.solve(g)
        catch err
        end
        solutions[name][v] = sol
    end
end

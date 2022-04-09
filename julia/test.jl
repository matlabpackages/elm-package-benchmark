using Solver
using JSON

# Read graph
compat, uuid_to_name = Solver.read_elm_graph("graph.json")

# Solve
@time solutions = Solver.solve_elm(compat, uuid_to_name)

open("result-julia.json", "w") do f
    JSON.print(f, solutions)
end

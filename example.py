from semver import Version
from semver import VersionRange
from semver import parse_constraint

from mixology.constraint import Constraint
from mixology.package_source import PackageSource as BasePackageSource
from mixology.range import Range
from mixology.union import Union

from mixology.version_solver import Union
from mixology.version_solver import VersionSolver

def print_decisions(decisions):
    for package, version in decisions.items():
        print(f'  {package}: {version}')

def print_solution(solver, result):
    if solver.is_solved():
        print('Solution found:')
        print_decisions(result.decisions)
    else:
        print('NO SOLUTION FOUND!')
        print('Attempts: ', result.attempted_solutions)
        print('Solved: ', solver.is_solved())
        raise ValueError('solving failed')

class Dependency:

    def __init__(self, name, constraint):  # type: (str, str) -> None
        self.name = name
        self.constraint = parse_constraint(constraint)
        self.pretty_constraint = constraint

    def __str__(self):  # type: () -> str
        return self.pretty_constraint


class PackageSource(BasePackageSource):

    def __init__(self):  # type: () -> None
        self._root_version = Version.parse("0.0.0")
        self._root_dependencies = []
        self._packages = {}

        super(PackageSource, self).__init__()

    @property
    def root_version(self):
        return self._root_version

    def add(
        self, name, version, deps=None
    ):  # type: (str, str, Optional[Dict[str, str]]) -> None
        if deps is None:
            deps = {}

        version = Version.parse(version)
        if name not in self._packages:
            self._packages[name] = {}

        if version in self._packages[name]:
            raise ValueError("{} ({}) already exists".format(name, version))

        dependencies = []
        for dep_name, spec in deps.items():
            dependencies.append(Dependency(dep_name, spec))

        self._packages[name][version] = dependencies

    def root_dep(self, name, constraint):  # type: (str, str) -> None
        self._root_dependencies.append(Dependency(name, constraint))

    def _versions_for(
        self, package, constraint=None
    ):  # type: (Hashable, Any) -> List[Hashable]
        if package not in self._packages:
            return []

        versions = []
        for version in self._packages[package].keys():
            if not constraint or constraint.allows_any(
                Range(version, version, True, True)
            ):
                versions.append(version)

        return sorted(versions, reverse=True)

    def dependencies_for(self, package, version):  # type: (Hashable, Any) -> List[Any]
        if package == self.root:
            return self._root_dependencies

        return self._packages[package][version]

    def convert_dependency(self, dependency):  # type: (Dependency) -> Constraint
        if isinstance(dependency.constraint, VersionRange):
            constraint = Range(
                dependency.constraint.min,
                dependency.constraint.max,
                dependency.constraint.include_min,
                dependency.constraint.include_max,
                dependency.pretty_constraint,
            )
        else:
            # VersionUnion
            ranges = [
                Range(
                    range.min,
                    range.max,
                    range.include_min,
                    range.include_max,
                    str(range),
                )
                for range in dependency.constraint.ranges
            ]
            constraint = Union.of(ranges)

        return Constraint(dependency.name, constraint)


# Now, we need to specify our root dependencies and the available packages.

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

#from mixology.version_solver import VersionSolver

solver = VersionSolver(source)
result = solver.solve()
print_solution(solver, result)

# Example
from util import read_json

g = read_json('graph.json')

source = PackageSource()

pkg = 'EngageSoftware/elm-engage-common'
ver = '3.1.0'

source.root_dep(pkg, ver)

def convert_constraints(deps):
    d = {}
    for k, v in deps.items():
        d[k] = convert_constraint(v)
    return d

def convert_constraint(vers):
    if ' <= v < ' in vers:
        lower, upper = vers.split(' <= v < ')
        return f'>={lower} <{upper}'
    elif ' <= v <= ' in vers:
        lower, upper = vers.split(' <= v <= ')
        return f'>={lower} <={upper}'
    else:
        raise ValueError(vers)

def add_deps(g, source, pkg, added):
    added.append(pkg)
    for ver in g[pkg]:
        deps = g[pkg][ver]
        source.add(pkg, ver, deps=convert_constraints(deps))
        for dep_pkg in deps:
            if dep_pkg not in added:
                add_deps(g, source, dep_pkg, added)

add_deps(g, source, pkg, [])

solver = VersionSolver(source)
result = solver.solve()
print_solution(solver, result)

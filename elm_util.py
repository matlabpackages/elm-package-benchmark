from use_mixology import PackageSource

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

def create_package_source(g, root_package, root_version):
    source = PackageSource()
    source.root_dep(root_package, root_version)
    add_deps(g, source, root_package, [])
    return source

def create_full_package_source(g):
    # create PackageSource of full universe (without root package)
    source = PackageSource()
    for pkg, versions in g.items():
        for ver, deps in versions.items():
            source.add(pkg, ver, deps=convert_constraints(deps))
    return source

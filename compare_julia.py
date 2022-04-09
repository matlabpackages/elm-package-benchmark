from util import read_json, write_json

data = read_json('result-julia.json')

d = {}
for name, vers in data.items():
    name_l = name.lower()
    if name_l != 'julia':
        d[name_l] = {}
        for ver, decisions in vers.items():
            d[name_l][ver] = {}
            for dec_name, dec_ver in decisions.items():
                if dec_name != name:
                    d[name_l][ver][dec_name] = dec_ver
            if len(d[name_l][ver]) == 0:
                d[name_l][ver] = None

write_json('./result-julia-final.json', d, sort_keys=True, indent=2)

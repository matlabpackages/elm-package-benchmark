import requests
import os
from util import write_json, read_json
import asyncio
import aiohttp


async def main():
    output = './graph.json'
    folder = 'registry'
    package_folder = folder + '/packages'
    packages = get_package_names()
    await download_packages(package_folder, packages)
    graph = get_graph_from_folders(package_folder, packages)
    missing = get_missing_packages(graph)
    while missing:
        for m in missing:
            print(f'missing: {m}')
        await download_packages(package_folder, missing)
        packages.extend(missing)
        graph = get_graph_from_folders(package_folder, packages)
        missing = get_missing_packages(graph)
    write_json(output, graph, indent=2, sort_keys=True)

def get_package_names():
    r = requests.get('https://package.elm-lang.org/search.json')
    data = r.json()
    n = len(data)
    print(f'found {n} packages')
    packages = [d['name'] for d in data]
    return packages

async def download_packages(folder, names):
    async with aiohttp.ClientSession() as client:
        tasks = []
        for name in names:
            #print(name)
            tasks.append(download_package(folder, client, name))
        await asyncio.gather(*tasks)

async def download_package(folder, client, name):
    #print(f'started: {name}')
    url = f'https://package.elm-lang.org/packages/{name}/releases.json'
    if '+' in name:
        raise ValueError('+ in name')
    folder_name = name.replace('/', '+')
    async with client.request('GET', url) as r:
        try:
            versions = await r.json()
        except aiohttp.client_exceptions.ContentTypeError:
            print(f'failed relases: {name}')
            versions = {'1.0.0': 0}  # fallback
        n_ver = len(versions.keys())
        for version in versions.keys():
            url = f'https://package.elm-lang.org/packages/{name}/{version}/elm.json'
            async with client.request('GET', url) as r:
                try:
                    ver_data = await r.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    print(f'failed: {name}={version}')
                    ver_data = {"dependencies": {}}  # fallback
                write_json(f'{folder}/{folder_name}/{version}.json', ver_data, indent=4, sort_keys=True)
        #print(f'downloaded: {name}: {n_ver} versions')

def get_graph_from_folders(folder, packages):
    graph = {}
    for name in packages:
        folder_name = name.replace('/', '+')
        graph[name] = {}
        for ver_file in os.listdir(f'{folder}/{folder_name}'):
            version = ver_file.replace('.json', '')
            ver_data = read_json(f'{folder}/{folder_name}/{ver_file}')
            graph[name][version] = ver_data['dependencies']
    return graph

def get_missing_packages(graph):
    missing = []
    for versions in graph.values():
        for deps in versions.values():
            for dep in deps.keys():
                if dep not in graph and dep not in missing:
                    missing.append(dep)
    return missing

if __name__ == '__main__':
    asyncio.run(main())

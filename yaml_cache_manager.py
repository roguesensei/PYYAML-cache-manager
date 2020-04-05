import os
import yaml

class YAMLCacheManager():

    def __init__(self, path):
        self.path = path

    def cache(self, key, data):
        cache_yaml(self.path, key, data)

    def get(self, key):
        return get_yaml(self.path, key)

    def remove(self, key):
        remove_yaml(self.path, key)


def cache_yaml(path, key, data):
    with open('{}{}.yml'.format(legislate_path(path), key), 'w+') as cache_file:
        yaml.dump(data, cache_file, default_flow_style=False)

def get_yaml(path, key):
    try:
        data = yaml.load(open('{}{}.yml'.format(legislate_path(path), key)))
        return data
    except:
        return None

def remove_yaml(path, key):
    os.remove('{}{}.yml'.format(legislate_path(path), key))

def legislate_path(path):
    if (path.startswith('/')):
        path = path[1:]
    if not (path.endswith('/')):
        path += '/'
    return path
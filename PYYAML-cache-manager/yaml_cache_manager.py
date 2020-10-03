import os
import yaml

class YAMLCacheManager():

    def __init__(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

        self.path = path

    def cache(self, key, data):
        '''Cache data in YAML format with assigned key'''
        cache_yaml(self.path, key, data)

    def get(self, key, acquire = None):
        '''Get cached YAML data by key'''
        return get_yaml(self.path, key, acquire)

    def remove(self, key):
        '''Remove cached YAML data by key'''
        remove_yaml(self.path, key)


def cache_yaml(path, key, data):
    '''Cache data in YAML format with assigned key'''
    with open('{}{}.yml'.format(legislate_path(path), key), 'w+') as cache_file:
        yaml.dump(data, cache_file, default_flow_style=False)

def get_yaml(path, key, acquire = None):
    '''Get cached YAML data by key'''
    try:
        data = yaml.load(open('{}{}.yml'.format(legislate_path(path), key)))
        if data is None:
            acquire_data = acquire()

            if acquire_data is not None:
                cache_yaml(path, key, acquire_data)
                data = acquire_data
        return data
    except FileNotFoundError:
        if acquire is None:
            return None

        acquire_data = acquire()

        if acquire_data is not None:
            cache_yaml(path, key, acquire_data)
        return acquire_data

def remove_yaml(path, key):
    '''Remove cached YAML data by key'''
    os.remove('{}{}.yml'.format(legislate_path(path), key))

def legislate_path(path):
    '''Ensure path is in correct format'''
    if (path.startswith('/')):
        path = path[1:]
    if not (path.endswith('/')):
        path += '/'
    return path
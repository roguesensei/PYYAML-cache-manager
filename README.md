# PYYAML-cache-manager
A cache manager for caching YAML files
## Contents
- [Requirements](Requirements)
### Requirements
- Python 3.5+
- PyYaml
Install PyYaml using pip:
```
pip install pyyaml
```
Alternatively, path into the repo root:
```
pip install -r .\requirements.txt
```
### Usage
#### Using module
Cache a Python class/object:
```py
import yaml_cache_manager as cacher

class Data:
    def __init__(self, data_id, data_name, data_hobbies):
        self.data_id = data_id
        self.data_name = data_name
        self.data_hobbies = data_hobbies


cache_path = 'cache/' # Location where the cached YAML files will be stored
DATA_KEY = 'data_{}' # Name of the file, used as a cache key. We will be formatting this
generic_data = Data(1, 'Greg', {
                       'hobby_1': 'Programming',
                       'hobby_2': 'Running'}) # Data to cache

# Cache data to the path
cacher.cache_yaml(cache_path, DATA_KEY.format(generic_data.data_id), generic_data)
```
Our cached file will be saved in YAML format as `data_1.yml`:
```yml
!!python/object:__main__.Data
data_hobbies:
  hobby_1: Programming
  hobby_2: Running
data_id: 1
data_name: Greg
```
Now, we can load that data:
```py
# Load cached data with the key
loaded_data = cacher.get_yaml(cache_path, DATA_KEY.format(generic_data.data_id))
print(loaded_data.data_name) # Will output "Greg"
```
When it's no longer needed, remove it:
```py
# Remove cached data by key
cacher.remove_yaml(cache_path, DATA_KEY.format(generic_data.data_id))
```
#### Using class
Alternatively you can accomplish the same functionality with an instance of the `YAMLCacheManager` class:
```py
from yaml_cache_manager import YAMLCacheManager

class Data:
    def __init__(self, data_id, data_name, data_hobbies):
        self.data_id = data_id
        self.data_name = data_name
        self.data_hobbies = data_hobbies

cacher = YAMLCacheManager('cache/') # path goes in the contructor instead

DATA_KEY = 'data_{}' # Name of the file, used as a cache key. We will be formatting this
generic_data = Data(1, 'Greg', {
                       'hobby_1': 'Programming',
                       'hobby_2': 'Running'}) # Data to cache

# Cache data to the path
cacher.cache(DATA_KEY.format(generic_data.data_id), generic_data)

# Load cached data with the key
loaded_data = cacher.get(DATA_KEY.format(generic_data.data_id))
print(loaded_data.data_name) # Will output "Greg"

# Remove cached data by key
cacher.remove(DATA_KEY.format(generic_data.data_id))
```
### Remarks
The `get()` method of the `YAMLCacheManager` class and the `get_yaml()` module method return `None` if there is no file found, thus you will need to handle it yourself. Example:
```py
def get_data_by_id(path, data_id):
    data = yaml_cache_manager.get_yaml(path, DATA_KEY.format(data_id))
    if data is None:
        # retrieve data with a query, as an example, here
        
        # then cache the queried data
        yaml_cache_manager.cache_yaml(path, DATA_KEY.format(data_id), queried_data)
        # before reloading it again
        data = yaml_cache_manager.get_yaml(path, DATA_KEY.format(data_id))
    return data
 ```
There is a bonus `legislate_path()` method used by the cache manager automatically, but you may use it yourself in your project where it may be useful. It will ensure there is no `/` at the beginning, and there is a `/` at the end. It takes a `path` paremeter and returns the `path` as a `string`
#### `legislate_path()` usage
```py
data = yaml.load(open('{}{}.yml'.format(yaml_cache_manager.legislate_path(path), key)))
```
All other methods within the module/class are `void` methods

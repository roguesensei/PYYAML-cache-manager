# PYYAML-cache-manager
A cache manager for caching YAML files
## Contents
1. [Requirements](#requirements)
2. [Usage](#usage)
    1. [Using module](#module)
    2. [Using class](#class)
3. [Acquire data if file not found](#acquire)
4. [Legislate path](#legislate)
### Requirements <a name="requirements"></a>
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
### Usage <a name="usage"></a>
#### Using module <a name="module"></a>
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
#### Using class <a name="class"></a>
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
### Acquire data if file not found <a name="acquire"></a>
Previously, the `get()` method of the `YAMLCacheManager` class and the standard `get_yaml()` method would return `None` if no file is found. However, you can now pass an optional `acquire` lambda method parameter which will excecute as the data acquisition before caching it.
### `acquire` parameter usage
```py
def get_employees():
    # Using the sqlite3 module as an example
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employee;')
    rows = cursor.fetchall()
    return rows

def get_employees_cache(path, key):
    # We pass in a lambda function as the acquire() parameter
    data = cacher.get_yaml(path, key, lambda : get_employees())
    return data
```
Note that if no data is found from the `acquire` method, no file will be cached.
### Legislate path <a name="legislate"><a/>
There is a bonus `legislate_path()` method used by the cache manager autmatically, but you may use it yourself in your project where it may be useful. It will ensure there is no `/` at the beginning, and there is a `/` at the end. It takes a `path` paremeter and returns the `path` as a `string`
#### `legislate_path()` usage
```py
data = yaml.load(open('{}{}.yml'.format(yaml_cache_manager.legislate_path(path), key)))
```

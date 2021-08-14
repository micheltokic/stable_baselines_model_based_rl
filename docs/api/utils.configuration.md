<!-- markdownlint-disable -->

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\configuration.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.configuration`






---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\configuration.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Configuration`
Utility class for loading, accessing and modifying the configuration file for this framework. 

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\configuration.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(file: str) → None
```

Create new object and load given configuration file. 




---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\configuration.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(key: str, default=None)
```

Get a specific value from the configuration by key. 



**Args:**
 
 - <b>`key`</b>:  The key to get the value for. For nested objects/ keys the point (.) is  used as separator. E.g. get('foo.bar'). 
 - <b>`default`</b>:  Default value to return, if the given key does not have a value assigned 



**Returns:**
 
 - <b>`any`</b>:  the value for the given key. 

---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\configuration.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_config_from_file`

```python
load_config_from_file(file: str)
```

Load and parse the given configuration (yaml) file into the internal dict. 

---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\configuration.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `save_config`

```python
save_config(file=None)
```

Save current (internal dict) state of the configuration to the given file. 

---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\configuration.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `set`

```python
set(key: str, val)
```

Set a specific value in the configuration by key. Required nested config objects are created, too. 



**Args:**
 
 - <b>`key`</b>:  The key to set the value for. For nested Objectes the point (.) is used as  separator. E.g. set('foo.bar', 12) 
 - <b>`val`</b>:  The value to set for the given key 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

<!-- markdownlint-disable -->

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\base.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.spaces.base`





---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\base.py#L80"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `generate_gym_box_space`

```python
generate_gym_box_space(dimensions=None, low=None, high=None) → Box
```

Create a gym box space and derive parameters from given arguments. Either a dimension must be given or the dimension must be derivable from the length of min/max values. 



**Args:**
 
 - <b>`dimensions`</b> (int):  Amount of dimensions the Box has (shape) 
 - <b>`low`</b>:  Single minimum value (for all dimenions) or list of minimum values. In the first case  the dimension parameter may not be None. 
 - <b>`high`</b>:  Single maximum value (for all dimenions) or list of maximum values. In the first case  the dimension parameter may not be None. 

Returns a Gym Box space with given dimensions and low/high values. 


---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\base.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SpaceType`
An enumeration. 





---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\base.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SpaceValue`
A SpaceValue represents a wrapper for a given gym space (like Box, or Discrete) and concrete values that can either be returnes as the respective "gym values" or as values matching the CSV input configuration (i.e., values mapped to respective columns = the internal library representation). The representation is, for example, different for Discrete (Gym: 2, internal library: [0,0,1,0]). This class enables convertions between both different representations. Subclasses implement the logic for specific gym environments. 

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\base.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    type: SpaceType = <SpaceType.OBSERVATION: 2>,
    value: List = [],
    column_names: List = None
) → None
```








---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\base.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `from_gym_space`

```python
from_gym_space(
    gym_space: Space,
    value,
    space_type: SpaceType = <SpaceType.OBSERVATION: 2>,
    column_names: List = None
)
```

Create new SpaceValue from gym_space, the respective value and the space type (action or observation). 

---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\base.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `generate_default_col_names`

```python
generate_default_col_names(
    type: SpaceType = <SpaceType.OBSERVATION: 2>,
    amount: int = 1
) → List[str]
```

Generate a set of x default column names where x = amount. Default names consist of one character ("A" for actinos, "X" for observations) and a increasing number per column. 



**Args:**
 
 - <b>`type`</b>:  Which type to create column names for (action / observation). 
 - <b>`amount`</b>:  Amount of column names to create. 

Returns a list of default column names. 

---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\base.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_column_dict`

```python
to_column_dict() → Dict
```

Map the values of the Space to the respective column names (of the input CSV data file). 



**Returns:**
 
 - <b>`dict`</b>:  A dict with the column names as keys and the respective space values as  dict-values. Column names are set during intialization. 

---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\base.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_gym_space`

```python
to_gym_space() → Tuple[Space, Any]
```

Return the gym space of this value and the corresponding value. 

---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\base.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_value_list`

```python
to_value_list()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

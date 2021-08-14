<!-- markdownlint-disable -->

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\factory.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.spaces.factory`





---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\factory.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `space_value_from_gym`

```python
space_value_from_gym(
    gym_space: Space,
    value,
    space_type: SpaceType = <SpaceType.OBSERVATION: 2>
) → SpaceValue
```

Create a SpaceValue instance from the given gym-space "type", the respective value and the type of the SpaceValue (action or observation). 



**Args:**
 
 - <b>`gym_space`</b>:  The space fo the gym environment (e.g., Discrete or Box) 
 - <b>`value`</b>:  (observed) value (shape must fit the gym_space "configuration"), e.g. no  value=2 for Discrete(2), since possible values would be 0, or 1. 
 - <b>`space_type`</b>:  type the space is used for (this is, e.g., used for default column name  generation) 

Returns SpaceValue for given gym_space and value. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

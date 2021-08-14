<!-- markdownlint-disable -->

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\box.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.spaces.box`






---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\box.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BoxSpaceValue`




<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\box.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    type: SpaceType = <SpaceType.OBSERVATION: 2>,
    value: List = [],
    column_names: List = None,
    low=None,
    high=None
) → None
```








---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\box.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `from_gym_space`

```python
from_gym_space(
    gym_space: Box,
    value,
    space_type: SpaceType = <SpaceType.OBSERVATION: 2>,
    column_names: List = None
)
```





---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\box.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_gym_space`

```python
to_gym_space() → Tuple[Box, Any]
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

<!-- markdownlint-disable -->

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\discrete.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.spaces.discrete`






---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\discrete.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DiscreteSpaceValue`




<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\discrete.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    type: SpaceType = <SpaceType.OBSERVATION: 2>,
    value: List = [],
    column_names: List = None
) → None
```








---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\discrete.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `from_gym_space`

```python
from_gym_space(
    gym_space: Discrete,
    value,
    space_type: SpaceType = <SpaceType.OBSERVATION: 2>,
    column_names: List = None
)
```





---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\utils\spaces\discrete.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_gym_space`

```python
to_gym_space() → Tuple[Discrete, int]
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

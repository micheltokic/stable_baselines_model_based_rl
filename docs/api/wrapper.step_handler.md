<!-- markdownlint-disable -->

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\wrapper\step_handler.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `wrapper.step_handler`






---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\wrapper\step_handler.py#L7"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `StepRewardDoneHandler`
The reward handler is responsible for calculating the reward for the current state and the action that lead to the current state (get_reward method). Additionally, it must implement a get_done method that returns True unless the "environment" should stop. Within the class access to the current state and action as well as a history of both is given. 

The default implementation uses configuration parameters to calculate the reward and whether the current episode is finished, or not (thus, proper configuration parameters are required if using the default implementation). It is ok to only overwrite one of both functions (get_reward / get_done) in a custom implementation and make use of the default implementation for the other method. 

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\wrapper\step_handler.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(config: Configuration = None)
```








---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\wrapper\step_handler.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_done`

```python
get_done(step: int) → bool
```





---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\wrapper\step_handler.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_reward`

```python
get_reward(step: int) → float
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

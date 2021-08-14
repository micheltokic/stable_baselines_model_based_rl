<!-- markdownlint-disable -->

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\wrapper\wrapped_model_env.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `wrapper.wrapped_model_env`






---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\wrapper\wrapped_model_env.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `WrappedModelEnv`
This class wraps a dynamic model (created with the stable_baselines_model_based_rl library) as an Gym environment. This allows to train any policy on the environment using the dynmaic model in the background for predicting the next state/observation for any given action. 

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\wrapper\wrapped_model_env.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    model_path,
    config: Configuration,
    step_handler: StepRewardDoneHandler = None,
    window_size=None
)
```






---

#### <kbd>property</kbd> unwrapped

Completely unwrap this env. 



**Returns:**
 
 - <b>`gym.Env`</b>:  The base non-wrapped gym.Env instance 



---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\wrapper\wrapped_model_env.py#L99"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `reset`

```python
reset()
```





---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\wrapper\wrapped_model_env.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `step`

```python
step(action)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

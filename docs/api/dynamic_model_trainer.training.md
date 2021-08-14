<!-- markdownlint-disable -->

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\dynamic_model_trainer\training.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `dynamic_model_trainer.training`




**Global Variables**
---------------
- **ROOT_DIR**

---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\dynamic_model_trainer\training.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sample_environment_and_train_dynamic_model`

```python
sample_environment_and_train_dynamic_model(
    gym_environment_name,
    episode_count,
    max_steps,
    output_path
)
```

Sampling data from a given gym environment and building and training a dynamic model for a given csv dataset retrieved from a csv dataset retrieved from a gym environment based on configurations specified in a yaml file. 



**Args:**
 
 - <b>`gym_environment_name`</b>:  Name of the gym environment from which data is sampled 
 - <b>`episode_count`</b>:  Number of episodes to be sampled for the dataset 
 - <b>`max_steps`</b>:  Maximum number of steps in an episode 



**Returns:**
 
 - <b>`lstm_model`</b>:  The lstm model trained on the given dataset 


---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\dynamic_model_trainer\training.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `build_and_train_dynamic_model`

```python
build_and_train_dynamic_model(
    data_path,
    config: Configuration,
    output_path='d:\\development\\stable_baselines_model_based_rl'
)
```

Builds and trains a dynamic model for a given csv dataset retrieved from a gym environment based on configurations specified in a yaml file 



**Args:**
 
 - <b>`data_path`</b>:  Name of the data file 
 - <b>`config`</b>:  Configuration Object that contains the given yaml Configuration 
 - <b>`output_path`</b>:  Directory path of training output 



**Returns:**
 
 - <b>`model`</b>:  The model trained on the given dataset 



**Todo:**
 * evaluation, plotting configuration into yaml file? 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

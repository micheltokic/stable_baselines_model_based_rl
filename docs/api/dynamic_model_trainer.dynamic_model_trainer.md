<!-- markdownlint-disable -->

<a href="..\..\stable_baselines_model_based_rl\dynamic_model_trainer\dynamic_model_trainer.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `dynamic_model_trainer.dynamic_model_trainer`





---

<a href="..\..\stable_baselines_model_based_rl\dynamic_model_trainer\dynamic_model_trainer.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sample_environment_and_train_dynamic_model`

```python
sample_environment_and_train_dynamic_model(
    gym_environment_name,
    episode_count,
    max_steps
)
```

Sampling data from a given gym environment and building and training a dynamic model for a given csv dataset retrieved from a csv dataset retrieved from a gym environment based on configurations specified in a yaml file. 



**Args:**
 
 - <b>`gym_environment_name`</b>:  Name of the gym environment from which data is sampled 
 - <b>`episode_count`</b>:  Number of episodes to be sampled for the dataset 
 - <b>`max_steps`</b>:  Maximum number of steps in an episode 
 - <b>`log`</b>:  Specifies whether logging is desired 
 - <b>`evaluate_model`</b>:  Specifies whether the evaluation of the model is desired 
 - <b>`plot_results`</b>:  Specifies whether plotting is desired 
 - <b>`export_model`</b>:  Specifies whether the export of the model is desired 



**Returns:**
 
 - <b>`lstm_model`</b>:  The lstm model trained on the given dataset 


---

<a href="..\..\stable_baselines_model_based_rl\dynamic_model_trainer\dynamic_model_trainer.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `build_and_train_dynamic_model`

```python
build_and_train_dynamic_model(data_file_name, config_file_name)
```

Builds and trains a dynamic model for a given csv dataset retrieved from a gym environment based on configurations specified in a yaml file 



**Args:**
 
 - <b>`data_file_name`</b>:  Shape of the input 
 - <b>`config_file_name`</b>:  Mean of the targets to determine dense layer length 
 - <b>`log`</b>:  Specifies whether logging is desired 
 - <b>`evaluate_model`</b>:  Specifies whether the evaluation of the model is desired 
 - <b>`plot_results`</b>:  Specifies whether plotting is desired 
 - <b>`export_model`</b>:  Specifies whether the export of the model is desired 



**Returns:**
 
 - <b>`lstm_model`</b>:  The lstm model trained on the given dataset 



**Todo:**
 * evaluation, plotting configuration into yaml file? 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

<!-- markdownlint-disable -->

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\sampler\gym_sampler.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `sampler.gym_sampler`




**Global Variables**
---------------
- **ROOT_DIR**

---

<a href="https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/stable_baselines_model_based_rl\sampler\gym_sampler.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sample_gym_environment`

```python
sample_gym_environment(
    gym_environment_name: str,
    episode_count=20,
    max_steps=100,
    output_path='d:\\development\\stable_baselines_model_based_rl\\sample_output'
)
```

Sample the given gym environment with the given amount of episodes and maximum steps per episode. 

Two files are created: 
  - A CSV file, containing the sampled data. 
  - A YAML file, containing the configuration that results from the sampled gym  environment, based on the sample_config.yaml file. 



**Args:**
 
 - <b>`gym_environment_name`</b>:  Name of the Gym-Environment to sample. 
 - <b>`epsiode_count`</b>:  Amount of episodes to use for the sampling. 
 - <b>`max_steps`</b>:  Maximum steps per episode allowed during sampling. 
 - <b>`output_path`</b>:  The directory the generated files get saved in 

Returns (path_to_csv_data_file, configuration object) 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

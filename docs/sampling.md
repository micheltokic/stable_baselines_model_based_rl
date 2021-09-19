# Gym Sampling

## General
The `sampler.gym_sampler` module provides the `sample_gym_environment` method, that can be used
to sample a given gym environement, store the data in a csv file and create a base configuration
to be used with this framework.  
For more details about how to use it, checkout the `example_usage` directory and the API
documentation.

## Example
```python
gym_sampler.sample_gym_environment(
    gym_environment_name='CartPole-v1',
    episode_count=10,
    max_steps=100,
    output_path='./sample_output',
    debug=True)
```

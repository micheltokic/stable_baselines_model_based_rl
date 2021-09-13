# Home / Introduction

A Model-Based Reinforcement Learning Extension for Stable Baselines.

## Overview
This library provides separate components/ building blocks for four
distinct tasks, namely:

- **Sampling Data from a Gym Environement**. This step may be not required, if
  you already have data you want to use to train a dynamic model with.
- **Train a dynamic Model**. Either use sampled data from previous step, or your
  own data to train a dynamic model.
- **Wrap dynamic model in Gym Environment**. The framework can wrap the trained
  model in a gym environemtn with proper action and oberservation space. You
  only need to define a few details about your input data 
- **Train Policy with Stable Baselines**. Use any stable baselines algorithm to
  to train a poliy against the wrapped gym environment. You only have to specify
  some kind of reward function.

Depending on your use-case, you may only use some specific parts of the library.


## Example Scripts
The following list describes what each of the example scripts does. You can find
these example scripts in the `example_usage` folder in the root of the source code
of this library
([LINK](https://github.com/micheltokic/stable_baselines_model_based_rl/tree/main/example_usage)).

- `full_application.py`: This script showcases the workflow of this library: It
  demonstrates sampling a gym environment, creating a dynamic model from the
  sampled data, training a policy with stable baselines against a wrapped
  gym env using the dynamic model, and finally running the policy against the
  original gym environment.
- `give_data_and_train.py`: Demonstration of how to create and train the dynamic
  model with given input data.
- `model_wrapping.py`: Demonstration of how to wrap a dynamic model as gym
  environment.
- `multiple_tests.py`: TODO
- `sample_config.yaml`: This is the example/base configuration file for the library.
- `sample_env.py`: Demonstration of how to sample a gym environment.
- `sample_env_and_train.py`: Simple script that samples and trains a respective
  gym environment for multiple gym environments.
- `sb_policy_creation_example.py`: Example how to create a stable baselines policy.
- `stable_baselines_against_wrapped_env.py`: Example how to train a stable baselines
  policy against a wrapped environment (i.e., one, that uses a dynamic model).
- `stable_baselines_test.py`: Example how to train a stable baselines policy against
  the "original" gym environments.

For some of these scripts to work you must change some settings, e.g. paths to
models (which have to be created by you before, too), etc.

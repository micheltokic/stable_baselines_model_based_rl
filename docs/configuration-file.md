# Configuration File

The configuration file is a yaml file containing all required parameters used by
different parts of the library.

Different sections of the file are used by different components of the library,
such as the sampler, or for creating the dynamic model. Thus, not all configuration
options may be required to be adjusted by you, depending on what features of
the framework/library you use.  
The sampler will also create a (template) configuration file, based on the gym
environment that has been sampled.

A template/ example configuration file can be [viewed here](https://github.com/micheltokic/stable_baselines_model_based_rl/blob/main/example_usage/sample_config.yaml).


## Gym Environment Sampling
todo


## Input Data Configuration

### Example
```yaml
input_config:
    action_cols:
        - A_0
        - A_1
    action_type: DISCRETE  # one of: DISCRETE, MULTI_DISCRETE, BOX
    discrete_colum_sets: null
    action_box_bounds:
        low: null
        high: null
    observation_cols:
        - X_0
        - X_1
        - X_2
        - X_3
    observation_bounds:
        low: null
        high: null
    input_file_name: 'train.csv'
```

### Configuration of Action Columns
List including all CSV-Headers of columns, that represent actions.
```yaml
input_config:
    action_cols:
        - A_0
        - A_1
    action_type: DISCRETE
    discrete_column_sets: null
    action_box_bounds: null
```
#### Type of Action
Either DISCRETE, MULTI_DISCRETE, or BOX.
For DISCRETE, all action columns represent of of the possible discrete actions. For MULTI_DISCRETE and BOX,
the respective configuration keys (`discrete_colum_sets`, `action_box_bounds`) must be additionally defined.
See explanations next.

#### Multi Discrete Action
**Note**: Multi-Discrete Actions are not yet supported!  
It must be specified, which columns belong to which discrete action:
```yaml
input_config:
    action_cols:
        - A_0_0
        - A_0_1
        - A_1_0
        - A_1_1
        - A_1_2
    action_type: MULTI_DISCRETE
    discrete_column_sets:
        - [ A_0_0, A_0_1 ]
        - [ A_1_0, A_1_1, A_1_2 ]
    action_box_bounds: null
```
This configuration would represent a multi discrete action consisting of two discrete actions. The first of which would have two discrete actions (A_0_0, A_0_1), the second would have three discrete actions (A_1_0, A_1_1, A_1_2).

#### Box Actions
The bounds of the input box must be specified by two lists: one for minimum values, one for
maximum values.  
```yaml
input_config:
    action_cols:
        - A_1
        - A_2
        - A_3
    action_type: BOX
    discrete_column_sets: null
    action_box_bounds:
        low: [-1, 3, 0]
        high: [0, 5, 3]
```
This configuration represents three input actions, the first of which is between -1 and 3, the
second between 3 and 5 and the third between 0 and 3.


## Dynamic Model Creation / Training
todo


## Model Wrapping
todo


## Policy Configuration
todo
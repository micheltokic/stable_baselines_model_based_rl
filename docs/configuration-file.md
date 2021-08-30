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
{==**Note**: Multi-Discrete Actions are not yet supported!==}  
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
TODO


## Model Wrapping
Configuration for the Model Wrapping is required for three parts of the wrapping: Reward-, Done-,
and Reset-Handling.

### Example
```yaml
model_wrapping:
    reward:
        type: CONSTANT  # one of CONSTANT, EVAL, or HANDLER
        value: 1.0
    done:
        type: CONSTANT  # one of CONSTANT, EVAL, or HANDLER
        value: 200
    reset:
        type: RANDOM  # one of RANDOM, STATIC, EPISODE_START, or HANDLER
        value:
            buffer: null
            current_state: null
        data_file: null
```

### Reward Configuration
Three different types of Reward Configurations exist: Constant, Eval, and
Handler Reward-Handling.

#### Constant Reward-Handling
Setting the `type` to `CONSTANT` requires to additionally set a `value` to a constant
float value. This is the constant reward given per step.  
```yaml
model_wrapping:
    reward:
        type: CONSTANT
        value: 4.5
```

#### Eval Reward-Handling
Setting the `type` to `EVAL` requires to additionally set a `value` to an eval expression
that is used to calculate the reward. The eval expression must be valid Python code. The
[Python eval-function](https://docs.python.org/3/library/functions.html#eval) is used for
the calculation, respectively the given value-string is applied on the eval-function.
Within the context of the eval-function (i.e., within the given string/expression) the
current (new) state (observation) and the applied action (that lead to the new state)
are available via variables. The names of the variables are the ones given in the input-
configuration of the configuration file (**action_cols**, **observation_cols**).  
```yaml
model_wrapping:
    reward:
        type: EVAL
        value: "(A_0 + A_1) / (X_0**2 * X_1)"
```

#### Handler Reward-Handling
If the `type` is set to `HANDLER`, the user is required to implement a custom handler
for reward-calulation, which allows a more complex calculation. For details, check out the
[docs section regarding the step handler](environment-wrapping.md#step-handler).  
```yaml
model_wrapping:
    reward:
        type: HANDLER
        value: null
```

### Done Configuration
Three different types of Done Configurations exist: Constant, Eval, and
Handler Done-Handling.

#### Constant Done-Handling
Setting the `type` to `CONSTANT` requires to additionally set a `value` to a constant
int value. This is the constant amount of steps after which each episode ends.  
```yaml
model_wrapping:
    done:
        type: CONSTANT
        value: 450
```

#### Eval Done-Handling
Setting the `type` to `EVAL` requires to additionally set a `value` to an eval expression
that is used to calculate the done-state. It behaves similar to the
[eval-reward calculation](#eval-reward-handling)
```yaml
model_wrapping:
    done:
        type: EVAL
        value: "(X_0 + X_1)**2 > 100"
```

#### Handler Done-Handling
If the `type` is set to `HANDLER`, the user is required to implement a custom handler
for done-calulation, which allows a more complex calculation. For details, check out the
[docs section regarding the step handler](environment-wrapping.md#step-handler).  
```yaml
model_wrapping:
    done:
        type: HANDLER
        value: null
```

### Reset Configuration
For different types of Reset-Handling exist: Random-, Static-, Episode-Start-,
and Handler-Handling.

#### Random Reset-Handling
If the `type` is set to `RANDOM` the built-in (randomn) sampling of gym environments
is used to create the reset state/observation. If using a window_size > 1 this
will most likely produce observations and actions that would not occur together
in the "regular environment". Thus, this handling is not accurate for larger
window_sizes.  
```yaml
model_wrapping:
    reset:
        type: RANDOM
        value: null
        data_file: null
```

#### Static Reset-Handling
If the `type` is set to `STATIC`, the same reset observation and state are used
for every reset. Depending on the window_size, a list of states must be given to
fill the buffer initally. Also, the current state/observation must be given. For
a window_size of 3, for example, 2 values for the buffer plus one current observation
must be given:  
```yaml
model_wrapping:
    reset:
        type: STATIC
        value:
            buffer:
              - [1, 0, 1.0, 2.0, 3.0]
              - [0, 1, 2.0, 3.0, 2.5]
            current_state: [0.5, 2.0, 1.0]
        data_file: null
```
Note, that the buffer includes action and observation values (in the given order),
while the current_state only consists of an observation.

#### Episode-Start Reset-Handling
If the `type` is set to `EPISODE_START`, the reset-state and observation is read
from a given data-file (format must equal the file used for training the modes; it
can also be the same file, of course). From the given file, one random episode is
chosen and used for the reset.
```yaml
model_wrapping:
    reset:
        type: EPISODE_START
        value: null
        data_file: "/path/to/the/data/file.csv"
```

#### Handler Reset-Handling
If the `type` is set to `HANDLER`, the user is required to implement a custom handler
for the calculation of reset states. This allows a more complex calculation. For details,
check out the [docs section regarding the reset handler](environment-wrapping.md#reset-handler).  
```yaml
model_wrapping:
    reset:
        type: HANDLER
        value: null
        data_file: null
```


## Policy Configuration
TODO

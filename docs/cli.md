# Command Line Interface
The command line interface (CLI) allows you to perform the crucial operations of this library using
your terminal. Three main operations are supported: Sampling a gym environment, training a dynamic
model, and training a stable baselines policy against the dynamic model.

This docs page only gives you an overview, for more details and help use the built-in help and
explanations. They can be shown with the `--help` flag for any command or subcommand.

The base command is named `sb-mbrl` and expects one of the below shown subcommands. An additional
command named `sb-mbrl-obtain-config-file` can be used to create a sample config file.


## Global Options
### Configuration File
The `sb-mbrl` command takes the option `--config` as the path to the config file to use. If it is
not specified, a file named `config.yaml` is expected in the current working directory.  
`--config` can be replaced by `-c`, too.

Usage: `sb-mbrl --config /path/to/my/config.yaml COMMAND [ARGS]`.

### Debug
Usage: `sb-mbrl --debug COMMAND [ARGS]`.

This enables some additional debug features and verbose outputs.


## Sampling a Gym Environment
Usage: `sb-mbrl sample [OPTIONS] OUTPUT_DIRECTORY`.

This command can be used to sample a gym environment name and store the ouput in the
`OUTPUT_DIRECTORY`. The name of the gym environment is read from the config file, unless a custom
one is defined via the `--gym-env-name` option.

Addtionally, amount of episodes and max-steps per episode can be defined by `--episodes` and
`max-steps` options.

Example:
```shell
sb-mbrl -c ./config/config.yaml --debug sample --gym-env-name CartPole-v1 \
                                               --episodes 10              \
                                               --max-steps 200
```


## Creating a dynamic Model
Usage: `sb-mbrl create-dynamic-model [OPTIONS] OUTPUT_DIRECTORY`.

This command can be used to train a dynamic model using the settings from the provided config. The
input data file is also read from the config, unless a custom one is specified via `--input-data`.

The resulting model files (and debug stuff: plots, tensorboard, etc.) are stored in
`OUTPUT_DIRECTORY`.



## Training a Stable Baselines Policy
Usage: `sb-mbrl train-stable-baselines-policy [OPTIONS] MODEL_PATH OUTPUT_DIRECTORY`.

This command can be used to train a Stable Baselines policy against a wrapped gym environment that
used a dynamic model created by this library. It takes the path to the model as the `MODEL_PATH`
argument and stores the stable baselines policy in the `OUTPUT_DIRECTORY`.

If custom step- or reset- handlers should be used, they must be implemented in a python file. For
details see explanations below.

Algorithm, policy and timesteps are obtained from the config file unless overwritten explicitly
via the respective option flags.


### Custom Step Handler
If you want to use a custom step handler, you must implement it in a python file that is
located in the working directory where you use the CLI.

Example:

```python
# wrapper.py
from stable_baselines_model_based_rl.wrapper.step_handler import StepRewardDoneHandler
import math

class CustomStepHandler(StepRewardDoneHandler):
    def get_done(self, step: int) -> bool:
        # Angle and x-position at which to fail the episode
        theta_threshold_radians = 12 * 2 * math.pi / 360
        x_threshold = 2.4

        cur_state = self.observation.to_value_list()
        x = cur_state[0]
        theta = cur_state[2]

        return bool(
            x < -x_threshold
            or x > x_threshold
            or theta < -theta_threshold_radians
            or theta > theta_threshold_radians
        )
```

Now, provide the `--wrapper-step-handler` flag and point it to the file (omit the .py extension):

```shell
sb-mbrl train-stable-baselines-policy \
    --wrapper-step-handler wrapper    \
    /path/to/dynamic_model/model.h5   \
    /path/to/output/the/sb_policy/to
```

### Custom Reset Handler
This works the same way as for custom step handlers, just use the `--wrapper-reset-handler` flag.
The handler class must be named **CustomResetHandler**.

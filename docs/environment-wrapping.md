# Create wrapped Gym Environment
The dynamic model that has been created using this library can be wrapped in an gym environment.
This allows to run any algorithm against it to learn a policy, e.g. with stable baselines.  
The `WrappedModelEnv` requires the model that is used to predict new states after applying certain
actions.

## Basic Configuration / Setup
The most basic wrapping may look like this:
```python
cfg = Configuration('path/to/config.yaml')
env = WrappedModelEnv('path/to/exported/model.h5', config=cfg)
```
This would use all default settings. However, especially for done and reward calculation you
should provide some more sophisticated settings or handlers.  
Reward- and Done-Calculations are handled by the so called **Step Handler**. Another handler,
called **Reset Handler**, takes care about resetting the environment. Both are described in more
detail below.

## Step Handler
The default implementation of the Step Handler offers a few possibilities to calculate the reward
and the done-state for a given (current) observation. For more details, see the respective section
in the documentation of the [configuration file](configuration-file.md#model-wrapping).  
For more sophisticated use cases, you can implement your own step handler (derive from the base
version!) and provide methods for calculating reward and the done state. For this, you have to
overwrite the `get_reward` and `get_done` method. It is ok to only overwrite one method and use
the default implementation for the other one. Both methods receive the current step number as
argument. Additionally, the step handler has access to the following for object/class variables:

- `self.observation`: The current observation of the environment.
- `self.action`: The last action performed, i.e., the action that lead to the current observation.
- `self.observation_history`: A list (history) with all former observations.
- `self.action_history`: A list (history) with all former applied actions.

Here is an example of how to implement a step handler (only get_done()) for the "CartPole-v1"
environment. It "clones" the framework behaviour for getting the done state:

```python
class CartPoleStepHandler(StepRewardDoneHandler):
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
model_file_path = '...'
config = Configuration('...')
step_handler = CartPoleStepHandler(config)
WrappedModelEnv(model_file_path, config, step_handler)
```

Also have a look at the scripts in the `example_usage` folder. Some example step handlers for
gym environments are also available in the
`stable_baselines_model_based_rl.wrapper.gym_step_handlers` module.

## Reset Handler
The default reset handler provides a few basic ways to reset an environment. Take a look at the
respective section in the documentation of the
[configuration file](configuration-file.md#model-wrapping).  
For most use cases, the `EPISODE_START` type might be sufficient.

For even more sophisticated use cases, you can implement your own reset handler and provide it to
the `WrappedModelEnv` constructor (via the `reset_handler` argument).  
Therefore, you must overwrite the `generate_reset_observation` method, which receives the
`action_space`, `observation_space` and `window_size` as inputs. It must return a tuple with a
buffer as first item and the current state as second item. The buffer must contain
`window_size - 1` items (i.e. observations), together with the current state it is used as first
input into the dynamic model / neural network for the prediction of the next state.

Checkout the API documentation and the default implementations in the `ResetHandler` for more
details.


## Using the Gym Environment
After you have initialized the wrapped gym environment, you can use it like any other gym
environment, too. E.g., you can train a stable baselines policy against it.  
For examples, checkout the `example_usage` directory.

The following is an example of wrapping a dynamic model that trained the CartPole-v1
environemnt. The custom step handler listed above is used.

```python
# Initialization
model_file_path = './path/to/model.h5'
config = Configuration('./path/to/config.yaml')
step_handler = CartPoleStepHandler(config)

env = WrappedModelEnv(model_file_path, config, step_handler=step_handler)
env.reset()

# Usage
observation, reward, done, info = env.step(1)
```

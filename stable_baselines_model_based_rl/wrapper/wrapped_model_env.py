import collections
from stable_baselines_model_based_rl.wrapper.reset_handler import ResetHandler
from typing import Any, Tuple

import gym
import numpy as np
import tensorflow as tf
from gym.spaces.box import Box
from gym.spaces.discrete import Discrete
from gym.spaces.space import Space

from stable_baselines_model_based_rl.utils.configuration import Configuration
from stable_baselines_model_based_rl.utils.spaces.base import SpaceType, SpaceValue, generate_gym_box_space
from stable_baselines_model_based_rl.utils.spaces.box import BoxSpaceValue
from stable_baselines_model_based_rl.utils.spaces.discrete import DiscreteSpaceValue
from stable_baselines_model_based_rl.utils.spaces.factory import space_value_from_gym
from stable_baselines_model_based_rl.wrapper.step_handler import StepRewardDoneHandler


class WrappedModelEnv(gym.Env):
    """
    This class wraps a dynamic model (created with the stable_baselines_model_based_rl library) as
    an Gym environment. This allows to train any policy on the environment using the dynmaic model
    in the background for predicting the next state/observation for any given action.
    """

    config: Configuration = None
    step_handler: StepRewardDoneHandler = None
    reset_handler: ResetHandler = None
    action_type = None
    model = None
    window_size = None
    state_buffer = None
    steps = 0
    current_state = None
    steps_over_done = None

    action_space_internal_cls = None
    obs_space_internal_cls = None
    action_cols = None
    observation_cols = None

    # flag to control, whether the step function expects the internal action format,
    # e.g., a list for distinct actions, or the gym format (one int in case of distinct
    # actions).
    use_internal_action_format = False

    def __init__(self, model_path, config: Configuration,
                 step_handler: StepRewardDoneHandler = None, reset_handler: ResetHandler = None,
                 window_size=None):
        super().__init__()
        self.config = config
        self.step_handler = (step_handler if step_handler is not None
                             else StepRewardDoneHandler(config))
        assert isinstance(self.step_handler, StepRewardDoneHandler), \
            f'Invalid class/object given as step_handler! {type(self.step_handler).__name__}'
        self.reset_handler = (reset_handler if reset_handler is not None
                              else ResetHandler(config))
        assert isinstance(self.reset_handler, ResetHandler), \
            f'Invalid class/object given as reset_handler! {type(self.reset_handler).__name__}'

        self.action_type = config.get('input_config.action_type')
        assert self.action_type in ['DISCRETE', 'MULTI_DISCRETE', 'BOX'], \
            f'Unsupported action type ({self.action_type}) in configuration file (input config)!'

        self.model = tf.keras.models.load_model(model_path, compile=False)
        self.window_size = (window_size if window_size is not None
                            else self.config.get('dynamic_model.training.lag', 1))
        self.state_buffer = collections.deque(maxlen=self.window_size)

        # action and observation space
        self.obs_space_internal_cls, self.observation_space = _get_observation_space(config)
        self.action_space_internal_cls, self.action_space = _get_action_space(config)

        self.action_cols = list(self.config.get('input_config.action_cols'))
        self.observation_cols = list(self.config.get('input_config.observation_cols'))

    def step(self, action):
        # state_buffer must at least contain all but one required items for the prediction
        assert len(self.state_buffer) >= self.window_size - 1, \
            "State Buffer doesn't contain enough items, did you call reset() initially?"

        self.steps += 1

        # Map action input to internal format if gym format is given
        if not self.use_internal_action_format:
            mapped_action: SpaceValue = self.action_space_internal_cls.from_gym_space(
                self.action_space, action, SpaceType.ACTION, self.action_cols)
            action = mapped_action.to_value_list()

        net_input = [*action, *self.current_state]
        self.state_buffer.append(np.float64(net_input))

        net_input_state = np.array([list(self.state_buffer)])
        net_output = self.model.predict(np.float64(net_input_state))[0]
        self.current_state = np.float64(net_output)

        # Create SpaceValues for observation and action
        obs_space_value = self.obs_space_internal_cls(SpaceType.OBSERVATION,
                                                      list(self.current_state),
                                                      self.observation_cols)
        action_space_value = self.action_space_internal_cls(SpaceType.ACTION, list(action),
                                                            self.action_cols)

        # Use Step Handler for reward and done calculation
        self.step_handler.observation = obs_space_value
        self.step_handler.observation_history.append(obs_space_value)
        self.step_handler.action = action_space_value
        self.step_handler.action_history.append(action_space_value)
        reward = self.step_handler.get_reward(self.steps)
        done = self.step_handler.get_done(self.steps)

        if done and self.steps_over_done is None:
            self.steps_over_done = 0
        elif self.steps_over_done is not None:
            self.steps_over_done += 1
            print('ALERT! Called step() even though episode is already done! '
                  f'{self.steps_over_done} steps over done! Behaviour is undefined!')

        return self.current_state, reward, done, {}

    def reset(self):
        self.step_handler.observation = None
        self.step_handler.action = None
        self.step_handler.observation_history = []
        self.step_handler.action_history = []
        self.steps_over_done = None

        self.state_buffer.clear()

        expected_current_state_length = space_value_from_gym(
            self.observation_space, self.observation_space.sample()).col_amount()
        expected_buf_item_length = expected_current_state_length + space_value_from_gym(
            self.action_space, self.action_space.sample()).col_amount()

        buffer, cur_state = self.reset_handler.generate_reset_observation(self.action_space,
                                                                          self.observation_space,
                                                                          self.window_size)
        assert len(buffer) == self.window_size - 1, \
            'Reset Handler generated buffer with incompatible size!'
        assert len(cur_state) == expected_current_state_length, \
            'Reset Handler generated invalid current state (incompatible length)!'

        for buf_item in buffer:
            assert len(buf_item) == expected_buf_item_length, \
                'Reset Handler generated buffer with at least one incompatible item!'
            self.state_buffer.append(np.float64(buf_item))
        self.current_state = np.float64(cur_state)
        self.steps = 0

        return self.current_state


def _get_observation_space(config: Configuration) -> Tuple[Any, Box]:
    """Generate a space-instance for the gym observation space based on the configuration."""

    low = config.get('input_config.observation_bounds.low')
    high = config.get('input_config.observation_bounds.high')
    dimensions = len(config.get('input_config.observation_cols'))
    return BoxSpaceValue, generate_gym_box_space(dimensions, low, high)


def _get_action_space(config: Configuration) -> Tuple[Any, Space]:
    """Generate a space-instance for the gym action space based on the configuration."""

    action_cols = config.get('input_config.action_cols')
    type = config.get('input_config.action_type')

    if type == 'DISCRETE':
        return DiscreteSpaceValue, Discrete(len(action_cols))
    elif type == 'MULTI_DISCRETE':
        raise NotImplementedError('No support yet for Multi-Discrete!')
    elif type == 'BOX':
        low = config.get('input_config.action_box_bounds.low')
        high = config.get('input_config.action_box_bounds.high')
        dimensions = len(action_cols)
        return BoxSpaceValue, generate_gym_box_space(dimensions, low, high)

import os
from random import randint
from typing import Tuple

import numpy as np
import pandas as pd
from gym.spaces.space import Space
from pandas.core.groupby.generic import DataFrameGroupBy

from stable_baselines_model_based_rl.utils.configuration import Configuration
from stable_baselines_model_based_rl.utils.spaces.factory import space_value_from_gym


class ResetHandler:
    """A ResetHandler generates the "reset-observation" state for a (wrapped) gym environment.

    The default implementation calculates the reset observation based on the configuration. Custom
    handlers must overwrite the generate_reset_state() method. Derived classes/handlers also have
    access to the user configuration via the config class variable.
    """

    config: Configuration

    def __init__(self, config: Configuration = None):
        self.config = config

    def generate_reset_observation(self, action_space: Space, observation_space: Space,
                                   window_size: int = 1) -> Tuple:
        """Generate and return a reset buffer and a current state for a gym environment.
        The returned buffer contains values for the given window_size minus 1, such that the
        wrapped gym environment can use the buffer plus the returned current state plus the first
        user (action) input to fill up to the required amount of items in the buffer.

        Params:
            action_space: The action space used by the gym environment.
            observation_space: The observation space used by the gym environment.
            window_size: The size of the buffer used by the model (neural network) of the wrapped
                gym environment.

        Returns tuple with buffer as first item and the current (observation) space as second item.
        """

        r_type = self.config.get('model_wrapping.reset.type')

        if r_type == 'RANDOM':
            return self._generate_random_reset_state(action_space, observation_space, window_size)
        elif r_type == 'STATIC':
            return self._generate_static_reset_state()
        elif r_type == 'EPISODE_START':
            return self._generate_episode_based_reset_state(window_size)
        elif r_type == 'HANDLER':
            raise NotImplementedError('With HANDLER as type for RESET state calculation, ' +
                                      'you must implement and provide your own Handler!')
        else:
            raise ValueError('Invalid RESET state calculation configuration!')

    def _generate_random_reset_state(self, action_space: Space, observation_space: Space,
                                     window_size: int) -> Tuple:
        """Use space sampling to generate random reset state."""
        return [
            [*space_value_from_gym(action_space, action_space.sample()).to_value_list(),
             *space_value_from_gym(observation_space, observation_space.sample()).to_value_list()]
            for _ in range(window_size - 1)
        ], space_value_from_gym(observation_space, observation_space.sample()).to_value_list()

    def _generate_static_reset_state(self) -> Tuple:
        """Read static reset state from user configuration."""
        buffer = self.config.get('model_wrapping.reset.value.buffer')
        current_state = self.config.get('model_wrapping.reset.value.current_state')
        return buffer, current_state

    def _generate_episode_based_reset_state(self, window_size: int) -> Tuple:
        """Read random episode start from data file as reset state."""

        action_col_names = self.config.get('input_config.action_cols')
        obs_col_names = self.config.get('input_config.observation_cols')
        data_file = self.config.get('model_wrapping.reset.data_file')
        assert data_file is not None and os.path.exists(data_file), \
            'Invalid data file given for episode based reset handler!'

        data: DataFrameGroupBy = pd.read_csv(data_file).groupby('EPISODE')
        episode_amount = len(data.groups)
        assert max(list(data.size())) >= window_size, \
            'Reset Handler: All episodes from data file are shorter than required window size!'

        while True:
            episode = randint(0, episode_amount - 1)
            episode_data = data.get_group(episode)[:window_size]
            if len(episode_data) >= window_size:
                break

        buffer_data = episode_data[:(window_size - 1)][[*action_col_names, *obs_col_names]]
        cur_state = episode_data[(window_size - 1):window_size][obs_col_names]
        return np.array(buffer_data), np.array(cur_state)[0]

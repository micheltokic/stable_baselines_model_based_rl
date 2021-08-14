from typing import List

from stable_baselines_model_based_rl.utils.spaces.base import SpaceValue
from stable_baselines_model_based_rl.utils.configuration import Configuration


class StepRewardDoneHandler:
    """
    The reward handler is responsible for calculating the reward for the current state and the
    action that lead to the current state (get_reward method). Additionally, it must implement a
    get_done method that returns True unless the "environment" should stop.
    Within the class access to the current state and action as well as a history of both is given.

    The default implementation uses configuration parameters to calculate the reward and whether
    the current episode is finished, or not (thus, proper configuration parameters are required
    if using the default implementation).
    It is ok to only overwrite one of both functions (get_reward / get_done) in a custom
    implementation and make use of the default implementation for the other method.
    """

    config: Configuration

    observation: SpaceValue
    action: SpaceValue
    observation_history: List[SpaceValue]
    action_history: List[SpaceValue]

    def __init__(self, config: Configuration = None):
        self.config = config

        self.observation = None
        self.action = None
        self.observation_history = []
        self.action_history = []

    def get_reward(self, step: int) -> float:
        r_type = self.config.get('model_wrapping.reward.type')
        r_value = self.config.get('model_wrapping.reward.value')

        if r_type == 'CONSTANT' and isinstance(r_value, (float, int)):
            return float(r_value)
        elif r_type == 'EVAL' and isinstance(r_value, str):
            global_args = {**self.observation.to_column_dict(), **self.action.to_column_dict()}
            result = eval(r_value, global_args)
            assert isinstance(result, (float, int)), 'REWARD eval must return number (int, float)!'
            return float(result)
        elif r_type == 'HANDLER':
            raise NotImplementedError('With HANDLER as type for REWARD calculation, you must ' +
                                      'implement and provide your own Handler!')
        else:
            raise ValueError('Invalid REWARD configuration!')

    def get_done(self, step: int) -> bool:
        d_type = self.config.get('model_wrapping.done.type')
        d_value = self.config.get('model_wrapping.done.value')

        if d_type == 'CONSTANT' and isinstance(d_value, int):
            return step >= int(d_value)
        elif d_type == 'EVAL' and isinstance(d_value, str):
            global_args = {**self.observation.to_column_dict(), **self.action.to_column_dict()}
            result = eval(d_value, global_args)
            assert isinstance(result, bool), 'DONE eval must return bool!'
            return result
        elif d_type == 'HANDLER':
            raise NotImplementedError('With HANDLER as type for DONE calculation, you must ' +
                                      'implement and provide your own Handler!')
        else:
            raise ValueError('Invalid DONE configuration!')

from typing import Any, List, Tuple
import numpy as np

from gym.spaces import Box
from stable_baselines_model_based_rl.utils.spaces.base import SpaceValue, SpaceType


class BoxSpaceValue(SpaceValue):
    dimensions: int = None
    low = None
    high = None

    def __init__(self, type: SpaceType = SpaceType.OBSERVATION, value: List = [],
                 column_names: List = None, low=None, high=None) -> None:
        super().__init__(type=type, value=value, column_names=column_names)
        self.dimensions = len(value)
        self.low = low if low is not None else -np.inf
        self.high = high if high is not None else np.inf

    @staticmethod
    def from_gym_space(gym_space: Box, value, space_type: SpaceType = SpaceType.OBSERVATION,
                       column_names: List = None):
        assert gym_space.shape[0] == len(value), 'Value length incompatible with box shape!'
        return BoxSpaceValue(space_type, value, column_names, gym_space.low, gym_space.high)

    def to_gym_space(self) -> Tuple[Box, Any]:
        return Box(low=self.low, high=self.high, shape=(self.dimensions,)), np.float32(self.value)

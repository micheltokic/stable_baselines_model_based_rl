from typing import List, Tuple
from gym.spaces import Discrete
from stable_baselines_model_based_rl.utils.spaces.base import SpaceValue, SpaceType


class DiscreteSpaceValue(SpaceValue):
    dimensions: int = None
    discrete_action_amount = None

    def __init__(self, type: SpaceType = SpaceType.OBSERVATION, value: List = [],
                 column_names: List = None) -> None:
        super().__init__(type=type, value=value, column_names=column_names)
        self.discrete_action_amount = len(value)

    @staticmethod
    def from_gym_space(gym_space: Discrete, value, space_type: SpaceType = SpaceType.OBSERVATION,
                       column_names: List = None):
        assert value >= 0 and value < gym_space.n, \
            'Given value incompatible with amount of discrete actions of given discrete space!'
        internal_value = [1 if x == value else 0 for x in range(gym_space.n)]
        return DiscreteSpaceValue(space_type, internal_value, column_names)

    def to_gym_space(self) -> Tuple[Discrete, int]:
        return Discrete(self.discrete_action_amount), self.value.index(1)

from gym.spaces.multi_discrete import MultiDiscrete
from stable_baselines_model_based_rl.utils.spaces.discrete import DiscreteSpaceValue
from gym.spaces.discrete import Discrete
from stable_baselines_model_based_rl.utils.spaces.base import SpaceType, SpaceValue
from stable_baselines_model_based_rl.utils.spaces.box import BoxSpaceValue
from gym.spaces.box import Box
from gym.spaces import Space as GymSpace


def space_value_from_gym(gym_space: GymSpace, value,
                         space_type: SpaceType = SpaceType.OBSERVATION) -> SpaceValue:
    """
    Create a SpaceValue instance from the given gym-space "type", the respective value and the type
    of the SpaceValue (action or observation).

    Args:
        gym_space: The space fo the gym environment (e.g., Discrete or Box)
        value: (observed) value (shape must fit the gym_space "configuration"), e.g. no
            value=2 for Discrete(2), since possible values would be 0, or 1.
        space_type: type the space is used for (this is, e.g., used for default column name
            generation)

    Returns SpaceValue for given gym_space and value.
    """

    space_class = None
    
    if isinstance(gym_space, Box):
        space_class = BoxSpaceValue
    elif isinstance(gym_space, Discrete):
        space_class = DiscreteSpaceValue
    elif isinstance(gym_space, MultiDiscrete):
        raise NotImplementedError('No support for MultiDiscrete, yet!')
    else:
        raise Exception('Unkown or not supported gym space!')

    return space_class.from_gym_space(gym_space, value, space_type)

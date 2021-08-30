import numpy as np

from enum import Enum
from gym.spaces import Space as GymSpace
from typing import Any, Dict, List, Tuple

from gym.spaces.box import Box


class SpaceType(Enum):
    ACTION = 1
    OBSERVATION = 2


class SpaceValue:
    """
    A SpaceValue represents a wrapper for a given gym space (like Box, or Discrete) and concrete
    values that can either be returnes as the respective "gym values" or as values matching the
    CSV input configuration (i.e., values mapped to respective columns = the internal library
    representation). The representation is, for example, different for Discrete (Gym: 2, internal
    library: [0,0,1,0]).
    This class enables convertions between both different representations. Subclasses implement
    the logic for specific gym environments.
    """

    type: SpaceType = None
    value = None
    column_names = None

    def __init__(self, type: SpaceType = SpaceType.OBSERVATION, value: List = [],
                 column_names: List = None) -> None:
        self.type = type
        self.value = value
        self.column_names = (column_names if column_names is not None
                             else SpaceValue.generate_default_col_names(type=type,
                                                                        amount=len(value)))
        assert len(self.value) == len(self.column_names), \
            'Amount of column names does not match length of value!'
    
    @staticmethod
    def from_gym_space(gym_space: GymSpace, value, space_type: SpaceType = SpaceType.OBSERVATION,
                       column_names: List = None):
        """Create new SpaceValue from gym_space, the respective value
           and the space type (action or observation)."""
        raise NotImplementedError

    def to_gym_space(self) -> Tuple[GymSpace, Any]:
        """Return the gym space of this value and the corresponding value."""
        raise NotImplementedError

    def to_column_dict(self) -> Dict:
        """Map the values of the Space to the respective column names (of the input CSV data file).

        Returns:
            dict: A dict with the column names as keys and the respective space values as
                dict-values. Column names are set during intialization.
        """
        return {col_name: self.value[i] for i, col_name in enumerate(self.column_names)}

    def to_value_list(self):
        return list(self.value)

    def col_amount(self):
        """Returns the required amount of columns for this space (value)."""
        return len(self.to_value_list())

    @staticmethod
    def generate_default_col_names(type: SpaceType = SpaceType.OBSERVATION,
                                   amount: int = 1) -> List[str]:
        """
        Generate a set of x default column names where x = amount. Default names consist of one
        character ("A" for actinos, "X" for observations) and a increasing number per column.

        Args:
            type: Which type to create column names for (action / observation).
            amount: Amount of column names to create.

        Returns a list of default column names.
        """
        prepend = 'X' if type == SpaceType.OBSERVATION else 'A'
        return [f'{prepend}_{i}' for i in range(amount)]


def generate_gym_box_space(dimensions=None, low=None, high=None) -> Box:
    """
    Create a gym box space and derive parameters from given arguments. Either a dimension
    must be given or the dimension must be derivable from the length of min/max values.

    Args:
        dimensions (int): Amount of dimensions the Box has (shape)
        low: Single minimum value (for all dimenions) or list of minimum values. In the first case
            the dimension parameter may not be None.
        high: Single maximum value (for all dimenions) or list of maximum values. In the first case
            the dimension parameter may not be None.

    Returns a Gym Box space with given dimensions and low/high values.
    """

    # either dimensions must be given or min/max must be lists of equal length
    assert (np.isscalar(dimensions) or 
            (isinstance(low, list) and isinstance(high, list) and len(low) == len(high)))

    dimensions = int(dimensions) if np.isscalar(dimensions) else len(low)
    
    if low is None or np.isscalar(low):
        v = low if low is not None else -np.inf
        low = [v for _ in range(dimensions)]
    if high is None or np.isscalar(high):
        v = high if high is not None else np.inf
        high = [v for _ in range(dimensions)]
    
    # replace any "null" values in a list of min/max with +/- inf
    low = [m if m is not None else -np.inf for m in low]
    high = [m if m is not None else +np.inf for m in high]

    return Box(low=np.array(low), high=np.array(high), shape=(dimensions,))

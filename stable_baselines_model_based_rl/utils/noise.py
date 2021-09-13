import random
import numpy as np
from numpy.core.arrayprint import DatetimeFormat


def add_gaussian_noise(data, columns, calc_mean=True, std=0, percentage=0.5):
    """
    Adds artificial gaussian noise to the data set in the given columns.

    Args:
        data: Dataset
        columns: Columns that are altered
        calc_mean: Specify if the generated noise should be based off of the mean value of a column or each column value on its own
        std: Standard deviation
        percentage: specifies how much of the data is modified by an artificial noise

    Returns:
        data: The noisy dataset
    """
    # always apply noise in the same rows (= noise_indices) on all observations
    noise_indices = random.sample(range(1, len(data)), int(len(data)*percentage))
    for col in columns:
        if calc_mean:
            col_mean = data[col].mean()
            noise = np.random.normal(col_mean, std, data[col].shape)
        else:
            noise = np.empty((data.shape[0]))
            # use every single observation value as mean, so that the noise is adequate to each value 
            for index, data_point in enumerate(data[col]): 
                noise[index] = np.random.normal(data_point, std, 1)[0]
        data[col].loc[noise_indices] += noise[noise_indices]
    return data

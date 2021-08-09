import random
import numpy as np
from numpy.core.arrayprint import DatetimeFormat


def add_fake_noise(data, observation_columns, noise):
    """
    Returns the dimension of a given gym (action/ observation)
    space.
    """
    noisy_data = data

    # pick random indices of the data to apply noise on
    # index amount max is half the data size
    amount = random.randint(0, int(len(noisy_data) / 2))
    indices = random.sample(range(0, len(noisy_data)), amount)
    for index in range(len(indices)):

        # pick random indices of the observation columns to apply noise on
        obs_amount = random.randint(0, len(observation_columns))
        obs_col_indices = random.sample(range(0, len(observation_columns)), obs_amount)
        for obs_col_index in range(len(obs_col_indices)):
            obs_col = observation_columns[obs_col_index]

            # alter value here
            if random.random() > 0.5:
                noisy_data[obs_col][index] += noise
            else:
                noisy_data[obs_col][index] -= noise

    return noisy_data

def add_gaussian_noise(data, observation_columns, calc_mean=True, mean=0, std=0, percentage=0.5):
    # always apply noise in rows (= noise_indices) on all column values (observations)
    noise_indices = random.sample(range(1, len(data)), int(len(data)*percentage))
    if calc_mean:
        for col in observation_columns:
            col_mean = data[col].mean()
            noise = np.random.normal(col_mean, std, data[col].shape)
            data[col].loc[noise_indices] += noise[noise_indices]
    else:
        noise = np.random.normal(mean, std, data[observation_columns].shape)
        data.loc[noise_indices] += noise[noise_indices]
    return data

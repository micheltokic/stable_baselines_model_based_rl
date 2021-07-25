import random

def add_fake_noise(data, observation_columns, noise):
    """
    Returns the dimension of a given gym (action/ observation)
    space.
    """
    noisy_data = data

    # pick random indices of the data to apply noise on
    # index amount max is half the data size
    amount = random.randint(0, int(len(noisy_data)/2))
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
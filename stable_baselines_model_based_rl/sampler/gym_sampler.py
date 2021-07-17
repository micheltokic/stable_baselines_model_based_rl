import datetime
import os
import gym
from gym.spaces import space
from gym.spaces.box import Box
from gym.spaces.discrete import Discrete
from gym.spaces.multi_discrete import MultiDiscrete
import pandas as pd
import yaml


def __get_dimension(space: space):
    """
    Returns the dimension of a given gym (action/ observation)
    space.
    """
    if isinstance(space, Discrete):
        return 1
    elif isinstance(space, Box):
        return space.shape[0]
    else:
        return 1


def __get_action_columns_and_sets(action_space: space):
    action_columns = []
    action_config = []
    
    if isinstance(action_space, Discrete):
        action_columns = [f'A_{i}' for i in range(action_space.n)]
        action_config = {
            'type': 'DISCRETE',
            'col_names': action_columns,
        }
    
    elif isinstance(action_space, MultiDiscrete):
        pass  # todo
    
    elif isinstance(action_space, Box):
        pass  # todo
    
    return action_columns, action_config


def __map_sampled_action_to_columns(action_space: space, action_config, sample_action):
    if isinstance(action_space, Discrete):
        assert action_config['type'] == 'DISCRETE'
        cols = action_config['col_names']
        values = [1 if i == sample_action else 0 for i in range(action_space.n)]
        return dict(zip(cols, values))
    
    elif isinstance(action_space, MultiDiscrete):
        pass  # todo

    elif isinstance(action_space, Box):
        pass  # todo


def __generate_config_yaml_file(action_cols, observation_cols, action_config,
                                output='./sampled_config_gym.yaml', data_file=None):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../sample_config.yaml')

    sample_config_file = open(path)
    config = yaml.full_load(sample_config_file)
    
    config['action_cols'] = action_cols
    config['observation_cols'] = observation_cols
    config['action_type'] = action_config['type']
    if data_file is not None:
        config['input_file_name'] = os.path.abspath(data_file)
    
    output_file = open(output, mode='w')
    yaml.dump(config, output_file)
    sample_config_file.close()
    output_file.close()
    
    return output_file


def sample_gym_environment(gym_environment_name: str, episode_count=20, max_steps=100):
    """
    Sample the given gym environment with the given amount of episodes and maximum
    steps per episode.

    Two files are created:
      - A CSV file, containing the sampled data.
      - A YAML file, containing the configuration that results from the sampled gym
        environment, based on the sample_config.yaml file.

    Args:
        gym_environment_name: Name of the Gym-Environment to sample.
        epsiode_count: Amount of episodes to use for the sampling.
        max_steps: Maximum steps per episode allowed during sampling.

    Returns (path_to_csv_data_file, path_to_yaml_config_file)
    """

    env = gym.make(gym_environment_name)
    # for details see: https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
    env.np_random.seed(0)

    action_col_names, action_config = __get_action_columns_and_sets(env.action_space)
    observation_space = env.observation_space

    ### PREPARE DATA FRAME
    d = {}
    # Counters for episode and step
    d["EPISODE"] = []
    d["STEP"] = []

    # action columns
    d.update({action_col: [] for action_col in action_col_names})
    
    # state/observation columns
    observation_col_names = []
    for i in range(0, __get_dimension(observation_space)):
        observation_name = f'X_{i}'
        d[observation_name] = []
        observation_col_names.append(observation_name)

    df = pd.DataFrame(data = d)

    ### SAMPLE DATA
    for episode in range (episode_count):
        print ("Start of episode %d" % episode)
        obs = env.reset()
        step = 0
        done = False
        
        while step < max_steps and not done:
            step += 1
            action = env.action_space.sample()

            df = df.append({
                'EPISODE': int(episode),
                'STEP': int(step),
                **__map_sampled_action_to_columns(env.action_space, action_config, action),
                **{observation_col_names[i]: obs[i] for i in range(0, len(observation_col_names))},
            }, ignore_index=True)
            
            obs, reward, done, _ = env.step(action)
            
        print ("  --> finished after %d steps" % step)
    
    df = df.astype({'EPISODE': int, 'STEP': int})
    time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../sample_output')

    #./ sample_output /
    data_file = f'{path}/{gym_environment_name.lower()}_{time}_sampled_data.csv'
    df.to_csv(data_file, sep=',', encoding='utf-8', index=False)

    config_file = f'{path}/{gym_environment_name.lower()}_{time}_config.yaml'
    __generate_config_yaml_file(action_col_names, observation_col_names, action_config,
                                output=config_file, data_file=data_file)

    return data_file, config_file

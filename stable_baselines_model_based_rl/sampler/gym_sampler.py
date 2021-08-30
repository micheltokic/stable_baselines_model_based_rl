import datetime
import os

import gym
import pandas as pd
from gym.spaces import space
from gym.spaces.box import Box
from gym.spaces.discrete import Discrete
from gym.spaces.multi_discrete import MultiDiscrete

from definitions import ROOT_DIR
from stable_baselines_model_based_rl.utils.configuration import Configuration
from stable_baselines_model_based_rl.utils.spaces.base import SpaceType
from stable_baselines_model_based_rl.utils.spaces.factory import space_value_from_gym


def __update_action_input_config(config: Configuration, action_space: space, action_col_names):
    if isinstance(action_space, Discrete):
        action_type = 'DISCRETE'
    elif isinstance(action_space, MultiDiscrete):
        action_type = 'MULTI_DISCRETE'
        raise NotImplementedError('Not yet supported!')  # TODO
    elif isinstance(action_space, Box):
        action_type = 'BOX'
        box_bounds = {
            'low': [float(x) for x in list(action_space.low)],
            'high': [float(x) for x in list(action_space.high)],
        }
        config.set('input_config.action_box_bounds', box_bounds)

    config.set('input_config.action_type', action_type)
    config.set('input_config.action_cols', action_col_names)


def __update_observation_input_config(config: Configuration, observation_cols, obs_space: Box):
    config.set('input_config.observation_cols', observation_cols)

    if isinstance(obs_space, Box):
        config.set('input_config.observation_bounds.low', [float(x) for x in list(obs_space.low)])
        config.set('input_config.observation_bounds.high',
                   [float(x) for x in list(obs_space.high)])


def __sample_gym_environment(gym_environment_name: str, episode_count=20, max_steps=100):
    config = Configuration(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        '../../example_usage/sample_config.yaml'))
    env = gym.make(gym_environment_name)
    # for details see: https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
    env.np_random.seed(0)
    env.action_space.np_random.seed(0)

    action_col_names = space_value_from_gym(env.action_space, env.action_space.sample(),
                                            SpaceType.ACTION).column_names
    observation_col_names = space_value_from_gym(env.observation_space,
                                                 env.observation_space.sample()).column_names
    __update_action_input_config(config, env.action_space, action_col_names)
    __update_observation_input_config(config, observation_col_names, env.observation_space)
    config.set('gym_sampling.gym_environment_name', gym_environment_name)

    # PREPARE DATA FRAME
    df = pd.DataFrame(data={
        'EPISODE': [],
        'STEP': [],
        **{col: [] for col in action_col_names + observation_col_names},
    })

    # SAMPLE DATA
    for episode in range(episode_count):
        print('Start of episode %d' % episode)
        obs = env.reset()
        step = 0
        done = False

        while step < max_steps and not done:
            step += 1
            action = env.action_space.sample()
            action_sv = space_value_from_gym(env.action_space, action, SpaceType.ACTION)
            obs_sv = space_value_from_gym(env.observation_space, obs)

            df = df.append({
                'EPISODE': int(episode),
                'STEP': int(step),
                **action_sv.to_column_dict(),
                **obs_sv.to_column_dict(),
            }, ignore_index=True)

            obs, reward, done, _ = env.step(action)

        print('  --> finished after %d steps' % step)

    df = df.astype({'EPISODE': int, 'STEP': int})
    return df, config


def sample_gym_environment(gym_environment_name: str, episode_count=20, max_steps=100,
                           output_path=os.path.join(ROOT_DIR, 'sample_output')):
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
        output_path: The directory the generated files get saved in

    Returns (path_to_csv_data_file, configuration object)
    """

    df, config = __sample_gym_environment(gym_environment_name, episode_count=episode_count,
                                          max_steps=max_steps)

    final_dir_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    final_dir_path = os.path.join(output_path, gym_environment_name, final_dir_name)
    os.makedirs(final_dir_path)

    data_file = f'{final_dir_path}/data.csv'
    df.to_csv(data_file, sep=',', encoding='utf-8', index=False)
    config.set('input_config.input_file_name', os.path.abspath(data_file))
    config.set('model_wrapping.reset.data_file', os.path.abspath(data_file))
    config.save_config(file=f'{final_dir_path}/config.yaml')

    print(f'Data and config saved in: {final_dir_path}')
    return data_file, config

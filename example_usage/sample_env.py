import os

from definitions import ROOT_DIR
from stable_baselines_model_based_rl.sampler import gym_sampler

gym_environment_name = 'CartPole-v1'
episode_count = 1000
max_steps = 100
output_path = os.path.join(ROOT_DIR, 'example_usage')

gym_sampler.sample_gym_environment(gym_environment_name, episode_count, max_steps, output_path)
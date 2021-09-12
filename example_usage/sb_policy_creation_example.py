#
# Example Script: Use the wrapper of this libaray for stable baselines policy
#                 creation. Can be used with any Gym environment.
#


import os

import gym
from stable_baselines_model_based_rl.sb_training.stable_baselines_poliy_trainer import train_stable_baselines_policy
from definitions import ROOT_DIR
from stable_baselines_model_based_rl.utils.configuration import Configuration

gym_name = 'CartPole-v1'
env = gym.make(gym_name)
env.reset()

config = Configuration(os.path.join(ROOT_DIR, 'example_usage', 'sample_config.yaml'))
config.set('sb_policy.reinforcement_learning_algorithm', 'PPO')
config.set('sb_policy.policy', 'MlpPolicy')
config.set('sb_policy.timesteps', 10_000)

policy_output = os.path.join(ROOT_DIR, 'sample_output', 'CartPole-v1')

ppo_sb_model = train_stable_baselines_policy(config, env, policy_output, True, True)

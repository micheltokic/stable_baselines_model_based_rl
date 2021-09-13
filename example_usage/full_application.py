##############################################################################################
# This Script showcases several applications of the library:                                 #
#   - How to sample a gym environment and create a dynamic model from it                     #
#   - Create a gym environment wrapping this dynamic model                                   #
#   - Train a Stable Baselines Policy against the wrapped gym environment and save/export it #
#   - Load the exported policy and run it against the original gym environment               #
##############################################################################################


import math
import os

import gym
from numpy.core.fromnumeric import mean, std
from stable_baselines3 import PPO

from definitions import ROOT_DIR
from stable_baselines_model_based_rl.dynamic_model_trainer.training import \
    build_and_train_dynamic_model
from stable_baselines_model_based_rl.sampler.gym_sampler import sample_gym_environment
from stable_baselines_model_based_rl.sb_training.stable_baselines_poliy_trainer import \
    train_stable_baselines_policy
from stable_baselines_model_based_rl.wrapper.gym_step_handlers import get_step_handler_for_gym_env
from stable_baselines_model_based_rl.wrapper.wrapped_model_env import WrappedModelEnv

# this is the name of the gym environment to use within this script
GYM_ENV = 'CartPole-v1'
# set this mode to either create the stable baselines policy (+ sampling, dynamic model creation,
# model wrapping, etc.) or to load an already created policy (file) and apply it against the
# original gym environment
MODE = 'CREATION'  # one of 'CREATION' or 'APPLICATION'

# Path to the policy file (created in the CREATION step)
POLICY_FILE = None
# Settings for the gym sampling
GYM_SAMPLING_SETTINGS = {
    'episodes': 500,
    'max_steps': 500,
}
# How many timesteps for policy learning
POLICY_TIMESTEPS = 10_000


def sample_create_and_train_ppo(gym_name: str, sample_settings: dict, policy_timesteps: int):
    output_path_sampling = os.path.join(ROOT_DIR, 'sample_output')
    output_path_model = os.path.join(ROOT_DIR, 'sample_output', gym_name)

    data, config = sample_gym_environment(gym_name, sample_settings['episodes'],
                                          sample_settings['max_steps'], output_path_sampling)
    dyn_model, _, model_file_path = build_and_train_dynamic_model(data, config,
                                                                  output_path_model, debug=False)
    step_handler = get_step_handler_for_gym_env(gym_name, config)
    env = WrappedModelEnv(model_file_path, config, step_handler)
    env.use_internal_action_format = False
    env.reset()

    # Train and export Stable Baselines PPO Model
    config.set('sb_policy.reinforcement_learning_algorithm', 'PPO')
    config.set('sb_policy.policy', 'MlpPolicy')
    config.set('sb_policy.timesteps', policy_timesteps)
    ppo_sb_model = train_stable_baselines_policy(config, env,
                                                 os.path.join(ROOT_DIR, 'sample_output', gym_name),
                                                 True, True)
    
    return ppo_sb_model


def apply_ppo_against_gym(gym_name: str, policy_file_path: str, iterations: int):
    loaded_model = PPO.load(policy_file_path)
    framework_env = gym.make(gym_name)
    step_counts = []

    for i in range(iterations):
        step = 0
        done = False
        obs = framework_env.reset()
        while not done:
            step += 1
            action, _state = loaded_model.predict(obs, deterministic=True)
            obs, reward, done, info = framework_env.step(action)
            framework_env.render()
        print(f'Next iteration/episode done after {step} steps...')
        step_counts.append(step)
        framework_env.reset()
        step = 0
    
    print(f'Maximum amount of steps was: {max(step_counts)}')
    print(f'Minimum amount of steps was: {min(step_counts)}')
    print(f'Mean of amount of steps was: {mean(step_counts)}')
    print(f'Std of amount of steps was: {std(step_counts)}')


if MODE == 'CREATION':
    sample_create_and_train_ppo(GYM_ENV, GYM_SAMPLING_SETTINGS, POLICY_TIMESTEPS)
elif MODE == 'APPLICATION':
    apply_ppo_against_gym(GYM_ENV, POLICY_FILE, 100)
else:
    print('Invalid Mode!')

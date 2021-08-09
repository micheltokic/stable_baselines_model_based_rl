from stable_baselines_model_based_rl.dynamic_model_trainer import training
import os
from definitions import ROOT_DIR

gym_environment_name = 'CartPole-v1'
episode_count = 1
max_steps = 100
output_path = os.path.join(ROOT_DIR, 'sample_output')

training.sample_environment_and_train_dynamic_model(gym_environment_name, episode_count, max_steps, output_path)
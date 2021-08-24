import os
from stable_baselines_model_based_rl.utils.configuration import Configuration
from stable_baselines_model_based_rl.dynamic_model_trainer import training
from definitions import ROOT_DIR

root_path = os.path.join(ROOT_DIR, os.path.join('example_usage', os.path.join('CartPole-v1', '2021-08-17-08-55-28')))
data_path = os.path.join(root_path, 'data.csv')

config_path = os.path.join(root_path, 'config.yaml')

config = Configuration(config_path)
output_path = os.path.join(ROOT_DIR, 'sample_output')

training.build_and_train_dynamic_model(data_path, config, output_path)
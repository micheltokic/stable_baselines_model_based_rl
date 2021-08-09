import os
from utils.configuration import Configuration
from stable_baselines_model_based_rl.dynamic_model_trainer import training
from definitions import ROOT_DIR

data_path = os.path.join(ROOT_DIR, os.path.join('example_usage', os.path.join('CartPole-v1', 'sample_data.csv')))
config_path = os.path.join(ROOT_DIR, os.path.join('example_usage', 'sample_config.yaml'))
config = Configuration(config_path)
output_path = os.path.join(ROOT_DIR, os.path.join('sample_output', os.path.join('CartPole-v1', 'test')))

training.build_and_train_dynamic_model(data_path, config, output_path)
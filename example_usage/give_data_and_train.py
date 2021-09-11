import os

from definitions import ROOT_DIR
from stable_baselines_model_based_rl.dynamic_model_trainer import training
from stable_baselines_model_based_rl.utils.configuration import Configuration


def give_data_and_train(gym_environment_name, data_path, config_path):
    config = Configuration(config_path)
    output_path_model = os.path.join(ROOT_DIR, 'sample_output',
                                     gym_environment_name, 'dynamic_models')
    training.build_and_train_dynamic_model(data_path, config, output_path_model)


if __name__ == '__main__':
    gym_name = 'CartPole-v1'
    dir = os.path.join(ROOT_DIR, 'sample_output', gym_name, '2021-09-11-22-44-18')
    data_path = os.path.join(dir, 'data.csv')
    config_path = os.path.join(dir, 'config.yaml')
    give_data_and_train(gym_name, data_path, config_path)

import os

from utils.configuration import Configuration

from dynamic_model_trainer import dynamic_model_trainer


sample = True
sample_name = 'cartpole-v1_2021-07-31-17-12-17'

if sample:
    gym_environment_name = 'CartPole-v1'
    episode_count = 20
    max_steps = 100
    dynamic_model_trainer.sample_environment_and_train_dynamic_model(gym_environment_name, episode_count, max_steps)
else:
    sample_output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../sample_output/')
    data_file_name = f'{sample_output_path}{sample_name}_sampled_data.csv'
    config_file_name = f'{sample_output_path}{sample_name}_config.yaml'
    config = Configuration(config_file_name)
    dynamic_model_trainer.build_and_train_dynamic_model(data_file_name, config)

import os
from stable_baselines_model_based_rl.utils.configuration import Configuration
from stable_baselines_model_based_rl.dynamic_model_trainer import training
from definitions import ROOT_DIR


def give_data_and_train(gym_environment_name, data_path, config_path, output_path=None):
    config = Configuration(config_path)

    if output_path is None:
        output_path = os.path.join(ROOT_DIR, 'sample_output')
        output_path = os.path.join(output_path, gym_environment_name)
        try:
            os.mkdir(output_path)
        except PermissionError:
            print(f'Permission Error: folder {output_path} could not be created')
        except FileExistsError:
            print(f'FileExists Error: folder {output_path} already exists')
        except:
            print(f'Error: folder {output_path} could not be created ')

    training.build_and_train_dynamic_model(data_path, config, output_path)


if __name__ == '__main__':
    gym_name = 'CartPole-v1'
    root_path = os.path.join(ROOT_DIR,
                             os.path.join('example_usage', os.path.join('CartPole-v1', '2021-08-17-08-55-28')))
    data_path = os.path.join(root_path, 'data.csv')

    config_path = os.path.join(root_path, 'config.yaml')
    give_data_and_train(gym_name, data_path, config_path)
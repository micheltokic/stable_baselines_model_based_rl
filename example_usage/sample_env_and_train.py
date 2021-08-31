from stable_baselines_model_based_rl.dynamic_model_trainer import training
import os
from definitions import ROOT_DIR, gym_simple_control_environment_names


def sample_env_and_train(gym_environment_name, episode_count=200, max_steps=100, output_path=None):
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

    training.sample_environment_and_train_dynamic_model(gym_environment_name, episode_count, max_steps, output_path)


if __name__ == '__main__':
    # envs.registry.all()

    for name in gym_simple_control_environment_names:
        sample_env_and_train(name)

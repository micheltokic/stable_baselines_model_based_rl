import os
from dynamic_model_trainer.training import __build_and_train_dynamic_model
from sampler.gym_sampler import __sample_gym_environment

from definitions import ROOT_DIR, gym_simple_control_environment_names

if __name__ == '__main__':

    names = gym_simple_control_environment_names
    names = ['Pendulum-v0', 'MountainCar-v0', 'CartPole-v1', 'MountainCarContinuous-v0', 'Acrobot-v1']

    episode_count = 200
    max_steps = 100

    for name in names:
        output_path = os.path.join(ROOT_DIR, 'sample_output')
        output_path = os.path.join(output_path, name)
        try:
            os.mkdir(output_path)
        except PermissionError:
            print(f'Permission Error: folder {output_path} could not be created')
        except FileExistsError:
            print(f'FileExists Error: folder {output_path} already exists')
        except:
            print(f'Error: folder {output_path} could not be created ')

        learning_rates = [(0.00001 * (10 ** i)) for i in range(1, 5)]
        batch_sizes = [(2 ** i) for i in range(3, 9)]

        df, config = __sample_gym_environment(name, episode_count, max_steps)

        config.set("dynamic_model.training.max_epochs", 100)
        config.set("dynamic_model.training.steps_per_epoch", 1000)

        for lr in learning_rates:
            config.set("dynamic_model.training.learning_rate", lr)
            __build_and_train_dynamic_model(df, config, output_path)

        for bs in batch_sizes:
            config.set("dynamic_model.training.batch_size", bs)
            __build_and_train_dynamic_model(df, config, output_path)

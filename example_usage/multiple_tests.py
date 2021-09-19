import os

from definitions import ROOT_DIR, gym_simple_control_environment_names
from stable_baselines_model_based_rl.dynamic_model_trainer.training import \
    build_and_train_dynamic_model
from stable_baselines_model_based_rl.sampler.gym_sampler import sample_gym_environment

if __name__ == '__main__':
    names = gym_simple_control_environment_names
    names = ['Pendulum-v0', 'MountainCar-v0', 'CartPole-v1', 'MountainCarContinuous-v0', 'Acrobot-v1']

    episode_count = 200
    max_steps = 100

    for name in names:
        output_path = os.path.join(ROOT_DIR, 'sample_output', name)
        os.makedirs(output_path, exist_ok=True)

        learning_rates = [(0.00001 * (10 ** i)) for i in range(1, 5)]
        batch_sizes = [(2 ** i) for i in range(3, 9)]

        data_file, config = sample_gym_environment(name, episode_count, max_steps, output_path,
                                                   debug=True)

        config.set("dynamic_model.training.max_epochs", 100)
        config.set("dynamic_model.training.steps_per_epoch", 1000)

        for lr in learning_rates:
            config.set("dynamic_model.training.learning_rate", lr)
            build_and_train_dynamic_model(data_file, config, output_path, debug=True)

        for bs in batch_sizes:
            config.set("dynamic_model.training.batch_size", bs)
            build_and_train_dynamic_model(data_file, config, output_path, debug=True)

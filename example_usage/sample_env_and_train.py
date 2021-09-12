import os

from definitions import ROOT_DIR, gym_simple_control_environment_names
from stable_baselines_model_based_rl.dynamic_model_trainer import training
from stable_baselines_model_based_rl.sampler.gym_sampler import sample_gym_environment


def sample_env_and_train(gym_environment_name, episode_count=300, max_steps=500, debug=True):
    output_path_sampling = os.path.join(ROOT_DIR, 'sample_output')
    output_path_model = os.path.join(ROOT_DIR, 'sample_output', 'dynamic_models')

    data, config = sample_gym_environment(gym_environment_name, episode_count,
                                          max_steps, output_path_sampling)
    training.build_and_train_dynamic_model(data, config, output_path_model, debug)

if __name__ == '__main__':
    for name in gym_simple_control_environment_names:
        sample_env_and_train(name, 10, 100)

import os
from datetime import datetime

from gym import Env

from stable_baselines_model_based_rl.sb_training import get_sb_class_for_algo
from stable_baselines_model_based_rl.utils.configuration import Configuration


def train_stable_baselines_policy(config: Configuration, env: Env, output_dir: str = None,
                                  export: bool = False, debug: bool = False):
    """Train a stable baselines policy/ create a respective model.
    This function is a simple utility to learn a stable baselines policy agains any given
    gym environment. Optionally supports saving/exporting the model into the given output
    directory.

    Args:
        config: (Library) configuration.
        env: Gym environemnt to learn the policy against.
        output_dir: Directory where to export the model to (optionally).
        export: Set to True, if model should be exported.
        debug: If set to True, verbose output of stable baselines is enabled.

    Returns:
        The stable baselines model.
    """
    algo = config.get('sb_policy.reinforcement_learning_algorithm', 'PPO')
    policy = config.get('sb_policy.policy', 'MlpPolicy')
    timesteps = config.get('sb_policy.timesteps', 100_000)

    sb_cls = get_sb_class_for_algo(algo)
    model = sb_cls(policy, env, verbose=(1 if debug else 0))
    model.learn(total_timesteps=timesteps)

    if export == True and output_dir is None:
        print('Skipping export, as no output directory is given!')
    else:
        env_cls_name = type(env).__name__
        str_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file = f'{env_cls_name}_{algo}_{policy}_{str_time}.zip'
        export_path = os.path.join(output_dir, 'stable_baselines_models', file)
        model.save(export_path)
        print(f'Stable Baselines Model/Policy has been exported to: {export_path}')

    return model

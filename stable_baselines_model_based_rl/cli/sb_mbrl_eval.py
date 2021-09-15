import os

import click
import gym
from numpy.core.fromnumeric import mean, std

from stable_baselines_model_based_rl.sb_training import get_sb_class_for_algo


@click.command(
    help='Evaluate a given stable baselines policy against a gym environment. You have to specify '
         'SB_ALGORITHM, the algorithm used by the policy (like PPO, AC2, etc.), as well as '
         'POLICY_PATH, which is the path to the zip-file of the exported stable baselines model. '
         'GYM_ENV_NAME is the name of the gym environment to evaluate the policy against.')
@click.argument('sb_algorithm')
@click.argument('policy_path')
@click.argument('gym_env_name')
@click.option(
    '-e', '--episodes', default=25, show_default=True,
    help='Amount of episodes to run.')
def evaluate_sb_policy_against_gym_env(sb_algorithm, policy_path, gym_env_name, episodes):
    """CLI command for stable baselines policy evaluation against ("real") gym env."""
    sb_cls = get_sb_class_for_algo(sb_algorithm.upper())
    policy_path = os.path.abspath(policy_path)

    model = sb_cls.load(policy_path)
    env = gym.make(gym_env_name)

    step_counts = []
    for i in range(episodes):
        step = 0
        done = False
        obs = env.reset()
        while not done:
            step += 1
            action, _state = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            env.render()
        click.echo(f'Next episode done after {step} steps...')
        step_counts.append(step)
        env.reset()
        step = 0

    click.echo(f'Maximum amount of steps was: {max(step_counts)}')
    click.echo(f'Minimum amount of steps was: {min(step_counts)}')
    click.echo(f'Mean of amount of steps was: {mean(step_counts)}')
    click.echo(f'Std of amount of steps was: {std(step_counts)}')

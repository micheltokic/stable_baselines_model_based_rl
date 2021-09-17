import importlib
import os

import click
from click.exceptions import Abort

from stable_baselines_model_based_rl.cli.context import CliContext
from stable_baselines_model_based_rl.dynamic_model_trainer.training import \
    build_and_train_dynamic_model
from stable_baselines_model_based_rl.sampler import gym_sampler
from stable_baselines_model_based_rl.sb_training.stable_baselines_policy_trainer import \
    train_stable_baselines_policy as sb_trainer
from stable_baselines_model_based_rl.utils.configuration import Configuration
from stable_baselines_model_based_rl.wrapper.wrapped_model_env import WrappedModelEnv


@click.group(
    help='Command Line Interface of the "Model Based Reinforcement Learning for Stable Baselines" '
         'library.')
@click.option(
    '-c', '--config',
    help='Path to configuration file. If not specified, the config file is assumed to be available'
         'in the current working directory as "config.yaml".',
    default='./config.yaml')
@click.option(
    '-d', '--debug', is_flag=True, default=False, show_default=True,
    help='Enable some debugging outputs/ features.')
@click.pass_context
def sb_mbrl(ctx, config, debug):
    """Base command (group) of the CLI interface."""
    config_path = os.path.abspath(config)
    try:
        cfg = Configuration(config_path)
    except FileNotFoundError:
        click.echo('Configuration File not available! Please specify via -c!')
        raise Abort

    cli_context = CliContext(cfg, debug)
    ctx.obj = cli_context


@click.command(
    help='Sample a Gym Environment and create a proper base configuration file for this library.')
@click.argument('output_directory')
@click.option(
    '-g', '--gym-env-name', default=None,
    help='Name of the gym environment to sample. If not specified, the one from the config file '
         'is used.')
@click.option(
    '--episodes', default=300, type=int, show_default=True,
    help='Amount of episodes to sample.')
@click.option(
    '--max-steps', default=800, type=int, show_default=True,
    help='Max steps per episode to sample.')    
@click.pass_obj
def sample(cli_context: CliContext, output_directory, gym_env_name, episodes, max_steps):
    """CLI command for sampling of a given gym environemnt."""
    if gym_env_name is None:
        gym_env_name = cli_context.config.get('gym_sampling.gym_environment_name', 'CartPole-v1')
    output_directory = os.path.abspath(output_directory)
    try:
        gym_sampler.sample_gym_environment(
            gym_environment_name=gym_env_name,
            episode_count=episodes,
            max_steps=max_steps,
            output_path=os.path.abspath(output_directory),
            debug=cli_context.debug)
    except Exception as e:
        click.echo(f'Could not sample environment: {e}')
    else:
        click.echo('Sampling Done!')


@click.command(
    help='Create a dynamic model from given input data and config.')
@click.argument('output_directory')
@click.option('-d', '--input-data', default=None,
    help='Path to the data file to use for creating the model. If not given, the file specified '
         'in the config file is used.')
@click.pass_obj
def create_dynamic_model(cli_context: CliContext, output_directory, input_data):
    """CLI command for creation of a dynamic model for given input data."""
    if input_data is None:
        input_data = cli_context.config.get('input_config.input_file_name', None)
    if input_data is None or not os.path.isfile(input_data):
        click.echo('Input data file cannot be read or is no file!')
        raise Abort
    output_directory = os.path.abspath(output_directory)

    build_and_train_dynamic_model(input_data, cli_context.config, output_directory,
                                  cli_context.debug)


@click.command(
    help='Train a Stable Baselines Policy against a wrapped Gym Environment that uses a dynamic '
         'model created with this libary.')
@click.argument('model_path')
@click.argument('output_directory')
@click.option(
    '--wrapper-step-handler', default=None,
    help='If you wish to use a custom step handler, you must declare/implement the step handler '
         'as class named "CustomStepHandler" placed in the file you specify for this option. It '
         'must be valid python code! Additionally, the constructor must be the same as in the '
         'default class/implementation. Step and Reset handler may be defined in the same file.')
@click.option(
    '--wrapper-reset-handler', default=None,
    help='If you wish to use a custom reset handler, you must declare/implement the reset handler '
         'as class named "CustomResetHandler" placed in the file you specify for this option. It '
         'must be valid python code! Additionally, the constructor must be the same as in the '
         'default class/implementation. Step and Reset handler may be defined in the same file.')
@click.option(
    '--sb-rl-algorithm', default=None, type=str,
    help='Overwrite the learning algorithm defined in the config file (Stable Baselines).')
@click.option(
    '--sb-policy', default=None, type=str,
    help='Overwrite the policy defined in the config file (Stable Baselines).')
@click.option(
    '--sb-timesteps', default=None, type=int,
    help='Overwrite the timestep amount defined in the config (Stable Baselines).')
@click.pass_obj
def train_stable_baselines_policy(cli_context: CliContext, model_path, output_directory,
                                  wrapper_step_handler, wrapper_reset_handler,
                                  sb_rl_algorithm, sb_policy, sb_timesteps):
    """CLI command for creation of a stable baselines policy agains a wrapped gym environment that
    uses a give dynamic model."""
    if wrapper_step_handler is not None:
        step_handler_module = importlib.import_module(wrapper_step_handler)
        step_handler = step_handler_module.CustomStepHandler(cli_context.config)
    else:
        step_handler = None

    if wrapper_reset_handler is not None:
        reset_handler_module = importlib.import_module(wrapper_reset_handler)
        reset_handler = reset_handler_module.CustomResetHandler(cli_context.config)
    else:
        reset_handler = None

    if sb_rl_algorithm is not None:
        cli_context.config.set('sb_policy.reinforcement_learning_algorithm', sb_rl_algorithm)
    if sb_policy is not None:
        cli_context.config.set('sb_policy.policy', sb_policy)
    if sb_timesteps is not None:
        cli_context.config.set('sb_policy.timesteps', sb_timesteps)

    output_directory = os.path.abspath(output_directory)

    env = WrappedModelEnv(model_path, cli_context.config, step_handler, reset_handler)
    env.use_internal_action_format = False
    env.reset()

    sb_trainer(cli_context.config, env, output_directory, export=True, debug=cli_context.debug)


sb_mbrl.add_command(sample)
sb_mbrl.add_command(create_dynamic_model)
sb_mbrl.add_command(train_stable_baselines_policy)

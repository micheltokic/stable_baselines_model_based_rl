from stable_baselines_model_based_rl.utils.configuration import Configuration
from stable_baselines_model_based_rl.wrapper.gym_step_handlers.acrobot import AcrobotStepHandler
from stable_baselines_model_based_rl.wrapper.gym_step_handlers.cartpole import CartPoleStepHandler
from stable_baselines_model_based_rl.wrapper.gym_step_handlers.continuous_mountain_car import \
    ContinuousMountainCarStepHandler
from stable_baselines_model_based_rl.wrapper.gym_step_handlers.mountain_car import \
    MountainCarStepHandler
from stable_baselines_model_based_rl.wrapper.gym_step_handlers.pendulum import PendulumStepHandler
from stable_baselines_model_based_rl.wrapper.step_handler import StepRewardDoneHandler


def get_step_handler_for_gym_env(gym_env_name: str, cfg: Configuration) -> StepRewardDoneHandler:
    """Return an example step handler for the given gym environemtn name, that uses the
    given config file."""

    if gym_env_name == 'Acrobot-v1':
        handler = AcrobotStepHandler(cfg)
    elif gym_env_name == 'CartPole-v1':
        handler = CartPoleStepHandler(cfg)
    elif gym_env_name == 'MountainCarContinuous-v0':
        handler = ContinuousMountainCarStepHandler(cfg)
    elif gym_env_name == 'MountainCar-v0':
        handler = MountainCarStepHandler(cfg)
    elif gym_env_name == 'Pendulum-v0':
        handler = PendulumStepHandler(cfg)
    else:
        raise NotImplementedError(f'No support for this gym env: {gym_env_name}')

    return handler

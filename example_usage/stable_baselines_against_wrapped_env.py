import os

from definitions import ROOT_DIR
from stable_baselines_model_based_rl.sb_training.stable_baselines_poliy_trainer import \
    train_stable_baselines_policy
from stable_baselines_model_based_rl.utils.configuration import Configuration
from stable_baselines_model_based_rl.wrapper.wrapped_model_env import WrappedModelEnv

cfg_path = './sample_output/CartPole-v1/loss=0.0002335651806788519-lag=4.00-2021-08-14-13-15-36/config.yaml'
model_path = './sample_output/CartPole-v1/loss=0.0002335651806788519-lag=4.00-2021-08-14-13-15-36/model.h5'
gym_env_name = 'CartPole-v1'

cfg = Configuration(cfg_path)
env = WrappedModelEnv(model_path, config=cfg)
env.use_internal_action_format = False
env.reset()

export_path = os.path.join(ROOT_DIR, 'sample_output', gym_env_name)
ppo_sb_model = train_stable_baselines_policy(cfg, env, export_path, True, True)

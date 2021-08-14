from stable_baselines_model_based_rl.utils.configuration import Configuration
from stable_baselines_model_based_rl.wrapper.wrapped_model_env import WrappedModelEnv


base_path = './sample_output/CartPole-v1/loss=0.0002335651806788519-lag=4.00-2021-08-14-13-15-36'

cfg = Configuration(f'{base_path}/config.yaml')
env = WrappedModelEnv(f'{base_path}/model.h5', config=cfg)

env.reset()
state1, reward1, done1, info1 = env.step(action=list([1, 0]))
state2, reward2, done2, info2 = env.step(action=list([0, 1]))
state3, reward3, done3, info3 = env.step(action=list([0, 1]))
state4, reward4, done4, info4 = env.step(action=list([1, 0]))
state5, reward5, done5, info5 = env.step(action=list([0, 1]))
state5, reward5, done5, info5 = env.step(action=list([1, 0]))

print('Done')

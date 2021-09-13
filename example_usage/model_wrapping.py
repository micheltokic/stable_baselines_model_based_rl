from stable_baselines_model_based_rl.utils.configuration import Configuration
from stable_baselines_model_based_rl.wrapper.wrapped_model_env import WrappedModelEnv


cfg_path = './sample_output/CartPole-v1/loss=0.0002335651806788519-lag=4.00-2021-08-14-13-15-36/config.yaml'
model_path = './sample_output/CartPole-v1/loss=0.0002335651806788519-lag=4.00-2021-08-14-13-15-36/model.h5'

cfg = Configuration(cfg_path)
env = WrappedModelEnv(model_path, config=cfg)

episodes = 100

for e in range(episodes):
    print(f'NEXT EPISODE {e}:')
    env.reset()
    step = 0

    while True:
        step += 1
        state, reward, done, info = env.step(env.action_space.sample())
        print('Step', step, '---', state, reward, done, info)

        if done:
            break

print('Done')

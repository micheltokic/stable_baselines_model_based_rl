#
# Example Script: Train PPO policy with stable baselines against Gym Environment
#

import gym
from stable_baselines3 import A2C, PPO


env = gym.make('Acrobot-v1')

# model = transitions/Environment without rewards/done and visualization
model = PPO('MlpPolicy', env, verbose=1)
#model = A2C('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=100000)

obs = env.reset()
for i in range(1000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()

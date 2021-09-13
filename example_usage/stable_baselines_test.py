#
# Example Script: Train PPO policy with stable baselines against Gym Environment
#

import gym
from numpy.core.fromnumeric import mean, std
from stable_baselines3 import A2C, PPO

env = gym.make('CartPole-v1')
episodes = 100

# model = transitions/Environment without rewards/done and visualization
model = PPO('MlpPolicy', env, verbose=1)
#model = A2C('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=100000)

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
    print(f'Next iteration/episode done after {step} steps...')
    step_counts.append(step)
    env.reset()
    step = 0

print(f'Maximum amount of steps was: {max(step_counts)}')
print(f'Minimum amount of steps was: {min(step_counts)}')
print(f'Mean of amount of steps was: {mean(step_counts)}')
print(f'Std of amount of steps was: {std(step_counts)}')

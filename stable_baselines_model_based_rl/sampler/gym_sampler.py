import gym
from gym.spaces import space
from gym.spaces.box import Box
from gym.spaces.discrete import Discrete
import pandas as pd


def get_dimension(space: space):
    """
    Returns the dimension of a given gym (action/ observation)
    space.
    """
    if isinstance(space, Discrete):
        return 1
    elif isinstance(space, Box):
        return space.shape[0]
    else:
        return 1


#SAMPLING
def sample_input_and_config(gym_environment_name, episode_count=20, max_steps=100):
    env = gym.make(gym_environment_name)
    # for details see: https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
    env.np_random.seed(0)

    action_space = env.action_space
    observation_space = env.observation_space

    env.reset()

    d = {}
    input_col_names = []

    for i in range(0, get_dimension(observation_space)):
        input_name = "X_" + str(i)
        d[input_name] = []
        input_col_names.append(input_name)

    d["EPISODE"] = []
    d["STEP"] = []
    d["ACTION"] = []

    df = pd.DataFrame(data = d)


    ### SAMPLE DATA
    for episode in range (episode_count):
        print ("Start of episode %d" % episode)
        obs = env.reset()
        step = 0
        done = False
        
        while step < max_steps and not done:
            step += 1
            action = env.action_space.sample()

            obs_dic = { input_col_names[i]: obs[i] for i in range(0, len(input_col_names)) }
            obs_dic["EPISODE"] = int(episode)
            obs_dic["STEP"] = int(step)
            obs_dic["ACTION"] = int(action)

            df = df.append(obs_dic, ignore_index=True)
            
            obs, reward, done, _ = env.step(action)
            
        print ("  --> finished after %d steps" % step)
    
    df.to_csv("data.csv", sep=',', encoding='utf-8', index=False)

    # return config_file, data_file


# Test
# sample_input_and_config('CartPole-v0')


def sample_input_file(gym_environment_name):
    """
    Sample given Gym Environment and create CSV file.

    Arguments:
        :gym_environemnt_name: 
    """
    pass
    #return data_file


def sample_input(gym_environment_name):
    pass
    #return data
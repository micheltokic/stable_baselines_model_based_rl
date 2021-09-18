from stable_baselines3 import A2C, DDPG, DQN, HER, PPO, SAC, TD3
from stable_baselines3.common.base_class import BaseAlgorithm


def get_sb_class_for_algo(algo: str) -> BaseAlgorithm:
    """Get the corresponding stable baselines class for the given algorithm name."""
    if algo == 'AC2':
        return A2C
    elif algo == 'DDPG':
        return DDPG
    elif algo == 'DQN':
        return DQN
    elif algo == 'HER':
        return HER
    elif algo == 'PPO':
        return PPO
    elif algo == 'SAC':
        return SAC
    elif algo == 'TD3':
        return TD3
    else:
        raise NotImplementedError(f'The {algo} sb algorithm is not yet supported!')

import numpy as np

from stable_baselines_model_based_rl.wrapper.step_handler import StepRewardDoneHandler


class PendulumStepHandler(StepRewardDoneHandler):
    max_speed = 8
    max_torque = 2.

    def get_reward(self, step: int) -> float:
        state = self.observation.to_value_list()
        th = state[0]  # th := theta
        thdot = state[1]
        u = self.action.to_value_list()[0]
        u = np.clip(u, -self.max_torque, self.max_torque)[0]
        costs = angle_normalize(th) ** 2 + .1 * thdot ** 2 + .001 * (u ** 2)
        return -costs


def angle_normalize(x):
    return (((x+np.pi) % (2*np.pi)) - np.pi)

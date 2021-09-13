from numpy import cos

from stable_baselines_model_based_rl.wrapper.step_handler import StepRewardDoneHandler


class AcrobotStepHandler(StepRewardDoneHandler):
    def get_done(self, step: int) -> bool:
        s = self.observation.to_value_list()
        return bool(-cos(s[0]) - cos(s[1] + s[0]) > 1.)

    def get_reward(self, step: int) -> float:
        reward = -1. if not self.get_done(step) else 0.
        return reward

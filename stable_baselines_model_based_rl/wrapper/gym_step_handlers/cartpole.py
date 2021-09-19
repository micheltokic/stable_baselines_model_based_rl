import math

from stable_baselines_model_based_rl.wrapper.step_handler import StepRewardDoneHandler


class CartPoleStepHandler(StepRewardDoneHandler):
    def get_done(self, step: int) -> bool:
        # Angle and x-position at which to fail the episode
        theta_threshold_radians = 12 * 2 * math.pi / 360
        x_threshold = 2.4

        cur_state = self.observation.to_value_list()
        x = cur_state[0]
        theta = cur_state[2]

        return bool(
            x < -x_threshold
            or x > x_threshold
            or theta < -theta_threshold_radians
            or theta > theta_threshold_radians
        )

    def get_reward(self, step: int) -> int:
        return 1






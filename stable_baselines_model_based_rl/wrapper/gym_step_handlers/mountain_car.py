from stable_baselines_model_based_rl.wrapper.step_handler import StepRewardDoneHandler


class MountainCarStepHandler(StepRewardDoneHandler):
    goal_position = 0.5
    goal_velocity = 0

    def get_done(self, step: int) -> bool:
        s = self.observation.to_value_list()
        position = s[0]
        velocity = s[1]

        # Convert a possible numpy bool to a Python bool.
        return bool(
            position >= self.goal_position and velocity >= self.goal_velocity
        )

    def get_reward(self, step: int) -> float:
        return -1

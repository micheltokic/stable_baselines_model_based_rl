from stable_baselines_model_based_rl.utils.configuration import Configuration


class CliContext:
    """A simple utility class holding the context for the different cli commands."""

    def __init__(self, config: Configuration, debug: bool) -> None:
        self.config = config
        self.debug = debug

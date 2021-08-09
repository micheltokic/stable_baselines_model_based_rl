import yaml


class Configuration:
    """Utility class for loading, accessing and modifying the configuration file for this framework."""

    file: str = None
    config: dict = None

    def __init__(self, file: str) -> None:
        """Create new object and load given configuration file."""
        self.load_config_from_file(file)


    def load_config_from_file(self, file: str):
        """Load and parse the given configuration (yaml) file into the internal dict."""
        self.file = file
        config_yaml_file = open(self.file)
        self.config = yaml.full_load(config_yaml_file)
        config_yaml_file.close()


    def save_config(self, file = None):
        """Save current (internal dict) state of the configuration to the given file."""
        if file is None:
            file = self.file
        self.file = file

        config_yaml_file = open(self.file, mode='w')
        yaml.dump(self.config, config_yaml_file)
        config_yaml_file.close()


    def get(self, key: str, default = None):
        """Get a specific value from the configuration by key.

        Args:
            key: The key to get the value for. For nested objects/ keys the point (.) is
                used as separator. E.g. get('foo.bar').
            default: Default value to return, if the given key does not have a value assigned

        Returns:
            any: the value for the given key.
        """
        keys = key.split('.')
        keys.reverse()
        item = self.config
        len_keys = len(keys)
        while len_keys > 0:
            next_key = keys.pop()
            if next_key not in item:
                return default
            elif len(keys) > 0:
                item = item[next_key]
            else:
                return item[next_key]


    def set(self, key: str, val):
        """Set a specific value in the configuration by key.
        Required nested config objects are created, too.

        Args:
            key: The key to set the value for. For nested Objectes the point (.) is used as
                separator. E.g. set('foo.bar', 12)
            val: The value to set for the given key
        """
        keys = key.split('.')
        keys.reverse()
        item = self.config
        while len(keys) > 0:
            next_key = keys.pop()
            if next_key not in item:
                item[next_key] = {}
            if len(keys) == 0:
                item[next_key] = val
            item = item[next_key]

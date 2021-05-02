import json
from .singleton import Singleton
from .constants import DEFAULT_LOG_LEVEL, CONFIG_FILE_NAME, DUMMY_PASSWORD, DUMMY_EMAIL


class Configurations(metaclass=Singleton):
    """To manage configurations from file."""

    def __init__(self):
        """To initiate Configuration class."""
        self.log_level_key = "logLevel"
        self.email_key = "email"
        self.password_key = "password"
        config_data = self._read_config_file(CONFIG_FILE_NAME)
        if config_data is None:
            # if config file doesnot exists, update class variable it to default configuration
            self.log_level = DEFAULT_LOG_LEVEL
            self.email = DUMMY_EMAIL
            self.password = DUMMY_PASSWORD
            # Also, update configuration file to default configuration
            data = {self.log_level_key: DEFAULT_LOG_LEVEL}
            self._update_config_file(CONFIG_FILE_NAME, data)
        else:
            # else, fetch the contents from file and update class variables accordingly
            self._fetch_configurations(config_data, CONFIG_FILE_NAME)

    def _read_config_file(self, file_name):
        """To read configurations from JSON file.

        Args:
            file_name (str): file name of configurations
        """
        try:
            with open(file_name, "r") as config:
                config_data = json.load(config)
                return config_data
        except OSError:
            return None
        except Exception:
            return None

    def _update_config_file(self, file, json_data):
        """To update configurations to JSON file.

        Args:
            file (str): file name
            json_data (dict): json data to be updated on file

        Returns:
            bool: Boolean representing status of task performed.
        """
        try:
            with open(file, "w") as f:
                json.dump(json_data, f)
                return True
        except OSError:
            return False
        except Exception:
            return False

    def _parse_log_level(self, config_data, config_file):
        """To parse the log level."""
        data = config_data[self.log_level_key]
        if data.upper() == "DEBUG":
            return "DEBUG"
        elif data.upper() == "INFO":
            return "INFO"
        elif data.upper() == "WARN":
            return "WARN"
        elif data.upper() == "ERROR":
            return "ERROR"
        elif data.upper() == "CRITICAL":
            return "CRITICAL"
        else:
            config_data[self.log_level_key] = DEFAULT_LOG_LEVEL
            self._update_config_file(config_file, config_data)
            return "INFO"

    def _fetch_configurations(self, config_data, config_file):
        """To fetch configurations from config file and update the class variables and
        file after parsing each variable with respective use-case.

        Args:
            config_data (json): Json data to be validated
            config_file (file): file name of configurations file.
        """
        # For LOG LEVEL configuration parameter, verify its correctness
        # and update the config.json file and class variables accordingly
        if (
            self.log_level_key in config_data
            and len(str(config_data[self.log_level_key]).strip()) > 0
        ):
            self.log_level = self._parse_log_level(config_data, config_file)
        else:
            self.log_level = DEFAULT_LOG_LEVEL

        if (
            self.email_key in config_data
            and len(str(config_data[self.email_key]).strip()) > 0
        ):
            self.email = str(config_data[self.email_key]).strip()
        else:
            self.email = DUMMY_EMAIL

        if (
            self.password_key in config_data
            and len(str(config_data[self.password_key]).strip()) > 0
        ):
            self.password = str(config_data[self.password_key]).strip()
        else:
            self.password = DUMMY_PASSWORD

        # Update the configuration file with consistent parameters
        config_data[self.log_level_key] = self.log_level
        config_data[self.email_key] = self.email
        config_data[self.password_key] = self.password
        self._update_config_file(config_file, config_data)

# utils/config_loader.py
import yaml

def load_config(file_path="config.yaml"):
    # """Load the YAML configuration file and return the configuration dictionary."""
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config
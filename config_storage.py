import os
import json
import keyring

# Path for storing the last used config file path.
CONFIG_CACHE_FILE = os.path.expanduser("~/.redexter_config.json")
# Service name for keyring storage.
KEYRING_SERVICE = "ReDexter_rclone_config"

def get_last_config_path():
    if os.path.exists(CONFIG_CACHE_FILE):
        try:
            with open(CONFIG_CACHE_FILE, "r") as f:
                data = json.load(f)
            return data.get("config_path")
        except Exception:
            return None
    return None

def set_last_config_path(config_path):
    data = {"config_path": config_path}
    try:
        with open(CONFIG_CACHE_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("Error saving config path:", e)

def get_config_password(config_path):
    """Retrieve the password from the OS keyring for the given config file."""
    return keyring.get_password(KEYRING_SERVICE, config_path)

def set_config_password(config_path, password):
    """Store the config password in the OS keyring for the given config file."""
    keyring.set_password(KEYRING_SERVICE, config_path, password)

def clear_config_full():
    """
    Clears the saved config path and removes the associated keyring password.
    This helps ensure that sensitive data is not retained.
    """
    config_path = get_last_config_path()
    if config_path:
        try:
            keyring.delete_password(KEYRING_SERVICE, config_path)
        except Exception as e:
            print("Error deleting keyring password:", e)
    if os.path.exists(CONFIG_CACHE_FILE):
        try:
            os.remove(CONFIG_CACHE_FILE)
        except Exception as e:
            print("Error clearing config file:", e)
import configparser
import os
import subprocess

from PyQt6.QtWidgets import QInputDialog, QLineEdit

def load_rclone_config(file_path, config_password=None):
    """
    Uses rclone API (via subprocess call to "rclone config show") to get the decrypted config.
    If config_password is provided, it is used; otherwise the user is prompted.
    """
    if config_password is None:
        pwd, ok = QInputDialog.getText(None, "Config Password",
                                       "Enter rclone config password (leave blank if none):",
                                       QLineEdit.EchoMode.Password)
        if not ok:
            raise ValueError("No config password provided.")
        config_password = pwd.strip()
    env = os.environ.copy()
    if config_password:
        env["RCLONE_CONFIG_PASS"] = config_password
    result = subprocess.run(["rclone", "config", "show", "--config", file_path],
                            capture_output=True, text=True, env=env)
    if result.returncode != 0:
        raise ValueError("rclone config show failed: " + result.stderr)
    return parse_config(result.stdout)

def parse_config(config_text):
    config = configparser.ConfigParser()
    config.read_string(config_text)
    return config

def get_crypt_remotes(config):
    """
    From a ConfigParser object, returns a dictionary mapping remote names
    to (password, salt) for remotes of type "crypt".
    """
    crypt_remotes = {}
    for section in config.sections():
        if config.get(section, "type", fallback="").strip().lower() == "crypt":
            obscured_pw = config.get(section, "password", fallback="").strip()
            obscured_pw2 = config.get(section, "password2", fallback="").strip()
            if obscured_pw:
                from crypto import reveal
                try:
                    real_pw = reveal(obscured_pw)
                except Exception:
                    real_pw = ""
                try:
                    real_pw2 = reveal(obscured_pw2) if obscured_pw2 else ""
                except Exception:
                    real_pw2 = ""
                crypt_remotes[section] = (real_pw, real_pw2)
    return crypt_remotes
import configparser
from dataclasses import dataclass, field
from typing import Optional

SUPPORTED_DISPLAYS = ["LG", "Roku"]

@dataclass
class AppConfig:
    debug_mode: Optional[bool] = False
    log_level: str = 'INFO'
    display_ip: Optional[str] = None
    display_port: Optional[int] = None
    display_make: Optional[str] = None
    display_host_input: Optional[str] = None
    behavior_switch_to_host_input_on_wake: Optional[str] = None
    behavior_sleep_on_display_off: Optional[str] = None
    # Add more fields as needed

def read_config(config_path='/etc/opt/nocecnp/config.ini') -> AppConfig:
    config = configparser.ConfigParser()
    config.read(config_path)

    display_make = config.get('Display', 'display_make', fallback=None)
    if display_make and display_make not in SUPPORTED_DISPLAYS:
        raise ValueError(f"Invalid display_make: {display_make}. Must be one of {SUPPORTED_DISPLAYS}")

    return AppConfig(
        debug_mode=config.getboolean('General', 'debug', fallback=False),
        log_level=config.get('General', 'log_level'),
        display_name=config.get('Display', 'display_name'),
        display_ip=config.get('Display', 'display_ip', fallback=None),
        display_port=config.getint('Display', 'display_port', fallback=None),
        display_make=config.get('Display', 'display_make', fallback=None),
        display_host_input=config.get('Display', 'display_host_input', fallback=None),
        behavior_switch_to_host_input_on_wake=config.get('Behavior', 'switch_to_host_input_on_wake', fallback=None),
        behavior_sleep_on_display_off=config.get('Behavior', 'sleep_on_display_off', fallback=None)
    )


from nocecnp.config import read_config

import sys
import requests
from time import sleep, time

def setup_display(config):
    display_make = config.display_make
    match display_make:
        case "LG": # Not implemented yet
            from nocecnp.lg_adapter import LGTV
            return LGTV(config)
        case "Roku":
            from nocecnp.roku_adapter import RokuTV
            return RokuTV(config)
        case _:
            raise ValueError(f"Unsupported display make: {display_make}")

def main():
    config = read_config()
    print(config)
    display = setup_display(config)

    display.power_on()
    sleep(10)
    display.power_off()

if __name__ == "__main__":
    main()
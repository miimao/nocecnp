from nocecnp.config import read_config
import asyncio
from time import sleep, time
import asyncio
from dbus_next.aio.message_bus import MessageBus
from dbus_next.constants import BusType
from dbus_next.constants import MessageType
from dbus_next.signature import Variant

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

async def watch_sleep_signals(display):
    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
    introspection = await bus.introspect('org.freedesktop.login1', '/org/freedesktop/login1')
    obj = bus.get_proxy_object('org.freedesktop.login1', '/org/freedesktop/login1', introspection)
    manager = obj.get_interface('org.freedesktop.login1.Manager')

    def on_prepare_for_sleep(sleeping):
        if sleeping:
            print("System is going to sleep, powering off display.")
            display.power_off()
        else:
            print("System woke up, powering on display.")
            display.power_on()

    manager.on_prepare_for_sleep(on_prepare_for_sleep)
    await asyncio.get_event_loop().create_future()  # Run forever

def main():
    config = read_config()
    print(config)
    display = setup_display(config)
    asyncio.run(watch_sleep_signals(display))

if __name__ == "__main__":
    main()
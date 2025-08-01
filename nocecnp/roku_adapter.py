from roku import Roku
from nocecnp.display import DisplayInterface

class RokuTV(DisplayInterface):
    def __init__(self, config):
        display_ip = config.display_ip
        # If port is None, use the default Roku port
        display_port = config.display_port or 8060
        print(display_port)
        self.wake_input = config.display_host_input
        self.roku = Roku(host=display_ip, port=display_port)

    def power_on(self):
        print("Sending Wakeup Command...")
        if not self.wake_input:
            self.roku.home()  # Default action if no specific input is set
        apps = {app.id: app for app in self.roku.apps}
        input_id = f"tvinput.{self.wake_input.lower()}"
        if input_id in apps:
            self.roku.launch(apps[input_id])
        else:
            print(f"Input '{self.wake_input}' not found among Roku inputs. Available: {list(apps.keys())}")
        
    def power_off(self):
        self.roku.poweroff()



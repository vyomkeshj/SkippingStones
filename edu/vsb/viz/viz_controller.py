import random
import threading
import time

from edu.vsb.viz.viz_screen import viz_screen


class viz_controller:
    def __init__(self):
        self.screen = viz_screen()
        x = threading.Thread(target=self.screen.run_world)
        x.start()

        y = threading.Thread(target=self.move_the_agent)
        y.start()

        while True:
            time.sleep(5)
            self.screen.add_dynamic_obstacles([(15, 15, 17)])
            self.screen.apply_impulse()

    def move_the_agent(self):
        while True:
            time.sleep(0.5)
            update_x = random.random()/2
            update_y = random.random()/2
            update_step = [update_x, update_y]
            self.screen.update_agent_position(update_step)


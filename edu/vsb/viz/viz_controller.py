import random
import threading
import time

from edu.vsb.viz.agent_target_generator import agent_target_generator
from edu.vsb.viz.viz_screen import viz_screen


class viz_controller:
    def __init__(self):
        self.screen = viz_screen()
        self.agent_pos, self.target_pos = None, None
        self.agent_target_generator = agent_target_generator(self.screen.world)
        self.reset_agent_and_target()

        self.dynamic_obstacle_count = 4
        x = threading.Thread(target=self.screen.run_world)
        x.start()

        y = threading.Thread(target=self.move_the_agent)
        y.start()

        while True:
            time.sleep(5)
            if self.dynamic_obstacle_count > 0:
                self.dynamic_obstacle_count = self.dynamic_obstacle_count-1
                self.screen.add_dynamic_obstacles([(15, 15, 17)])
            self.screen.apply_impulse()
            self.reset_agent_and_target()

    def reset_agent_and_target(self):
        self.agent_target_generator.generate_agent_target_pair()
        self.agent_pos, self.target_pos = self.agent_target_generator.get_current_agent_target()
        self.screen.add_agent_and_target([self.agent_pos.position[0], self.agent_pos.position[1]], [self.target_pos.position[0], self.target_pos.position[1]])

    def move_the_agent(self):
        while True:
            time.sleep(0.5)
            update_x = random.random()/2
            update_y = random.random()/2
            update_step = [update_x, update_y]
            self.screen.update_agent_position(update_step)


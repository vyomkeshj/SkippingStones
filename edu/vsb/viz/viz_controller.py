import random
import threading
import time

import numpy as np

from edu.vsb.viz.agent_target_generator import agent_target_generator
from edu.vsb.viz.obstacles.static_obstacle_placement_strategy import static_obstacle_placement_strategy
from edu.vsb.viz.viz_screen import viz_screen
from Box2D.b2 import polygonShape


class viz_controller:
    def __init__(self):
        self.screen = viz_screen()
        self.static_obstacle_prov = static_obstacle_placement_strategy()

        self.agent_pos, self.target_pos = None, None
        self.agent_target_generator = agent_target_generator(self.screen.world)
        self.dynamic_obstacle_count = 3
        self.reset_agent_and_target()

        x = threading.Thread(target=self.screen.run_world)
        x.start()

        y = threading.Thread(target=self.move_the_agent)
        y.start()

        while True:
            time.sleep(5)
            if self.dynamic_obstacle_count > 0:
                self.dynamic_obstacle_count = self.dynamic_obstacle_count-1
            self.screen.apply_impulse()
            self.reset_agent_and_target()

    def reset_agent_and_target(self):
        self.screen.reset_screen()

        self.screen.add_dynamic_obstacles([(14, 20, 17)])
        self.screen.add_dynamic_obstacles([(11, 17, 23)])

        self.generate_random_obstacles()
        self.screen.apply_impulse()

        self.agent_target_generator.generate_agent_target_pair()
        self.agent_pos, self.target_pos = self.agent_target_generator.get_current_agent_target()
        self.generate_static_blockade()

        self.screen.add_agent_and_target([self.agent_pos.position[0], self.agent_pos.position[1]], [self.target_pos.position[0], self.target_pos.position[1]])

    def generate_static_blockade(self):
        agent_init = np.array([self.agent_pos.position[0], self.agent_pos.position[1]])
        target_init = np.array([self.target_pos.position[0], self.target_pos.position[1]])

        st_obstacles = self.static_obstacle_prov.get_obstacles(agent_init, target_init)
        for obstacle in st_obstacles:
            item = self.screen.world.CreateStaticBody(
                position=obstacle[0],
                shapes=polygonShape(box=(obstacle[1], obstacle[1])),
                angle=obstacle[2]
            )
            self.screen.add_static_obstacles(item)

    def generate_random_obstacles(self):
        gen_cnt = self.dynamic_obstacle_count
        while gen_cnt > 0:
            pos_x = random.random() * 10
            pos_y = random.random() * 10
            angle = random.random() * 3.14

            self.screen.add_dynamic_obstacles([(pos_x, pos_y, angle)])
            gen_cnt = gen_cnt-1

    # later, use this to control the agent from the agent
    def move_the_agent(self):
        while True:
            time.sleep(0.5)
            update_x = random.random()/2
            update_y = random.random()/2
            update_step = [update_x, update_y]
            self.screen.update_agent_position(update_step)


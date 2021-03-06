import random
import threading
import time

import numpy as np

from edu.vsb.viz.agent_target_generator import agent_target_generator
from edu.vsb.viz.obstacles.object_meta import object_meta
from edu.vsb.viz.obstacles.static_obstacle_placement_strategy import static_obstacle_placement_strategy
from edu.vsb.viz.viz_screen import viz_screen
from Box2D.b2 import polygonShape


class viz_controller:
    def __init__(self):
        self.screen = viz_screen()
        self.static_obstacle_prov = static_obstacle_placement_strategy()
        self.static_obstacle_pos = np.array([])

        self.agent_pos, self.target_pos = None, None
        self.agent_target_generator = agent_target_generator(self.screen.world)
        self.dynamic_obstacle_count = 3
        self.reset_agent_and_target()

        x = threading.Thread(target=self.screen.run_world)
        x.start()
        # y = threading.Thread(target=self.move_the_agent_random)
        # y.start()

        # while True:
        #     time.sleep(3)
        #     self.screen.apply_random_impulse()
        #     self.reset_agent_and_target()

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

            self.static_obstacle_pos = np.array([obstacle[0][0], obstacle[0][1], obstacle[1], obstacle[2]])
            object_metadata = object_meta(400)
            item.userData = object_metadata
            self.screen.add_static_obstacles(item)

    def generate_random_obstacles(self):
        gen_cnt = self.dynamic_obstacle_count
        while gen_cnt > 0:
            pos_x = random.random() * 10
            pos_y = random.random() * 10
            angle = random.random() * 3.14

            self.screen.add_dynamic_obstacles([(pos_x, pos_y, angle)])
            gen_cnt = gen_cnt - 1

    # later, use this to control the agent from the agent
    def move_the_agent_random(self):
        while True:
            time.sleep(0.1)
            update_x = random.random() * 50
            update_y = random.random() * 50
            update_step = [update_x, update_y]

            self.screen.update_agent_position(update_step)

    # methods for gym wrapper

    def move_the_agent_gym(self, action):
        self.screen.update_agent_position(action)

    def get_reward_gym(self):
        done_status, collision_status = self.screen.get_flags_done_collision()
        # print("state array = ", self.get_state_array())
        if self.screen.reached_target:
            return 300
        elif collision_status:
            return -300
        else:
            return -1 - self.screen.get_agent_target_distance() / 30

    def get_pixel_matrix_gym(self):
        return self.screen.get_image()

    def get_state_array(self):
        dynamic_obs_states = self.screen.get_dynamic_obstacle_states()

        position_agent = self.screen.agent_target_pair[0].position
        position_target = self.screen.agent_target_pair[1].position

        position_agent_n = np.array((position_agent[0], position_agent[1]))
        position_target_n = np.array((position_target[0], position_target[1]))

        state_array = np.concatenate((dynamic_obs_states, self.static_obstacle_pos,
                                      position_agent_n, position_target_n), axis=None)

        normalized_v = state_array / np.sqrt(np.sum(state_array ** 2))
        return state_array

    def get_flags_done_collision_gym(self):
        return self.screen.get_flags_done_collision()

    def reset_agent_and_target(self):
        self.screen.reset_screen()  # deletes obstacles and adds walls

        self.generate_random_obstacles()
        self.screen.apply_random_impulse()

        self.agent_target_generator.generate_agent_target_pair()
        self.agent_pos, self.target_pos = self.agent_target_generator.get_current_agent_target()
        self.generate_static_blockade()

        self.screen.add_agent_and_target([self.agent_pos.position[0], self.agent_pos.position[1]],
                                         [self.target_pos.position[0], self.target_pos.position[1]])

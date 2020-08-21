import math

import gym
import numpy as np
import torch

from edu.vsb.viz.viz_controller import viz_controller


class gym_environment(gym.Env):

    def __init__(self):
        self.action_count = 0
        self._max_episode_steps = 300

        self.action_space = gym.spaces.Box(low=np.array([-1.0000, -1.0000]),
                                           high=np.array([1.0000, 1.0000]),
                                           dtype=np.float32)
        self.previous_experience = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0])
        self.observation_buffer_size = 4      #history size
        self.single_observation_size = 17
        self.observation_size = self.single_observation_size * self.observation_buffer_size
        self.observation_buffer = torch.zeros(self.observation_size)
        # self.observation_space = gym.spaces.Box(low=0, high=255, shape=(STATE_W, STATE_H, HISTORY), dtype=np.uint8)
        self.observation_space = gym.spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0, 0, 0, 0, 0
                          ],
                         dtype=np.float32),
            high=np.array([32, 24, math.pi, 32, 24, math.pi, 32, 24, math.pi, 32, 24, 3, math.pi, 32, 24, 32, 24,
                           32, 24, math.pi, 32, 24, math.pi, 32, 24, math.pi, 32, 24, 3, math.pi, 32, 24, 32, 24,
                           32, 24, math.pi, 32, 24, math.pi, 32, 24, math.pi, 32, 24, 3, math.pi, 32, 24, 32, 24,
                           32, 24, math.pi, 32, 24, math.pi, 32, 24, math.pi, 32, 24, 3, math.pi, 32, 24, 32, 24]),
            dtype=np.float32)
        self.environment = viz_controller()

    def get_net_observation(self, current_observation, flush):
        local_buffer = torch.cat((self.observation_buffer[self.single_observation_size: self.observation_size], current_observation))
        self.observation_buffer = local_buffer
        if flush:
            self.observation_buffer = torch.zeros(self.observation_size)

        return local_buffer

    def step(self, action):
        # depending on the action size, append zeros to it for rest of the joint to signify static joints using np.pad
        # print("action received = ", action)
        self.environment.move_the_agent_gym(action)
        done_status, has_collided = self.environment.get_flags_done_collision_gym()
        image_matrix = self.environment.get_pixel_matrix_gym()
        image_matrix = self.rgb2gray(image_matrix)

        state_received = self.environment.get_state_array()
        reward_received = self.environment.get_reward_gym()

        if has_collided is True or self.action_count > self._max_episode_steps:
            self.environment.reset_agent_and_target()
            self.action_count = 0

        return self.get_net_observation(torch.from_numpy(state_received), False), reward_received, done_status, {}

    def reset(self):
        self.environment.reset_agent_and_target()
        image_matrix = self.environment.get_pixel_matrix_gym()
        image_matrix = self.rgb2gray(image_matrix)
        state_received = self.environment.get_state_array()

        return self.get_net_observation(torch.from_numpy(state_received), False) # on reset, the observation is only the state of the environment

    def render(self, mode='human'):
        pass

    def rgb2gray(self, rgb):
        r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray

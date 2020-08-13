import gym
import numpy as np

from edu.vsb.viz.viz_controller import viz_controller

STATE_H = 480
STATE_W = 640


class gym_environment(gym.Env):

    def __init__(self):
        self.action_count = 0
        self._max_episode_steps = 100

        self.action_space = gym.spaces.Box(low=np.array([-10.0000, -10.0000]),
                                           high=np.array([10.0000, 10.0000]),
                                           dtype=np.float32)

        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(STATE_W, STATE_H, 3), dtype=np.uint8)
        self.environment = viz_controller()

    def step(self, action):
        # depending on the action size, append zeros to it for rest of the joint to signify static joints using np.pad
        self.environment.move_the_agent_gym(action)
        done_status, has_collided = self.environment.get_flags_done_collision_gym()
        image_matrix = self.environment.get_pixel_matrix_gym()
        reward_received = self.environment.get_reward_gym()

        if has_collided is True:
            self.environment.reset_agent_and_target()
        return image_matrix, reward_received, done_status, {}

    def reset(self):
        self.environment.reset_agent_and_target()
        image_matrix = self.environment.get_pixel_matrix_gym()

        return image_matrix  # on reset, the observation is only the state of the environment

    def render(self, mode='human'):
        pass

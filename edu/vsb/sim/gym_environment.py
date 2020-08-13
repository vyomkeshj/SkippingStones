import gym
import numpy as np
import torch

STATE_H = 480
STATE_W = 640


class gym_environment(gym.Env):

    def __init__(self):
        self.action_count = 0;
        self._max_episode_steps = 100

        self.action_space = gym.spaces.Box(low=np.array([-4.0000, -4.0000, -4.0000, -4.0000, -4.0000, -4.0000]),
                                           high=np.array([4.0000, 4.0000, 4.0000, 4.0000, 4.0000, 4.0000]),
                                           dtype=np.float32)

        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(STATE_H, STATE_W, 3), dtype=np.uint8)

    def step(self, action):
        # depending on the action size, append zeros to it for rest of the joint to signify static joints using np.pad
        num_zeros_to_append = self.robot_mdp.dof - self.num_active_joints
        action = np.pad(action, (0, num_zeros_to_append), 'constant')

        # print("action done = ",action)
        observation = self.robot_mdp.update_angle(action)
        # return <angles and vec difference>, <reward>, <done_status>. The first n_dof elements are angles, next observation_not_angles_size are vec difference
        observed_angles = observation[0:self.num_active_joints]
        observed_difference = observation[self.robot_mdp.dof: (self.robot_mdp.dof + self.observation_not_angles_size)]
        net_obs = torch.cat((observed_angles, observed_difference))
        # print("net observation = ",net_obs)
        reward_received = observation[self.single_observation_size]
        done_status = observation[self.single_observation_size + 1]
        # print("action = ", action, "observation = ", net_obs, "done =", done_status)
        # print("stepping ", action)
        return self.get_net_observation(net_obs, False), reward_received, done_status, {}

    def reset(self):
        observation = self.robot_mdp.reset_robot()

        observed_angles = observation[0:self.num_active_joints]

        observed_difference = observation[self.robot_mdp.dof: (self.robot_mdp.dof + self.observation_not_angles_size)]
        net_obs = torch.cat((observed_angles, observed_difference))

        return self.get_net_observation(net_obs, True)  # on reset, the observation is only the state of the environment

    def render(self, mode='human'):
        pass

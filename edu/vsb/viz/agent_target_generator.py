import random
from Box2D.b2 import polygonShape
import numpy as np

def get_random_point_in_polygon(bounds):
    minx, miny, maxx, maxy = bounds
    p = (random.uniform(minx, maxx), random.uniform(miny, maxy))
    return p


# generates and keeps the reference to the current agent and target
class agent_target_generator:
    def __init__(self, world, dist_range=None, border_margin=3):
        if dist_range is None:
            dist_range = [5, 10]
        self.world = world
        self.agent = None
        self.target = None
        self.border_margin = border_margin  # 3
        self.dist_range = dist_range
        self.world_bounds = (3, 3, 20, 20)
        self.min_dist = 7

        self.generate_agent_target_pair()

    def generate_agent_target_pair(self):

        dist = 0
        while dist < self.min_dist:
            agent_coords = get_random_point_in_polygon(self.world_bounds)
            target_coords = get_random_point_in_polygon(self.world_bounds)

            np_agent_pos = np.array(agent_coords)
            np_target_pos = np.array(target_coords)
            dist = np.linalg.norm(np_target_pos - np_agent_pos)

        print("current distance = ", dist)
        self.agent = self.world.CreateStaticBody(position=(agent_coords[0], agent_coords[1]),
                                                 shapes=polygonShape(box=(0.5, 0.5)))
        self.target = self.world.CreateStaticBody(position=(target_coords[0], target_coords[1]),
                                                  shapes=polygonShape(box=(0.5, 0.5)))

    def get_current_agent_target(self):
        return self.agent, self.target




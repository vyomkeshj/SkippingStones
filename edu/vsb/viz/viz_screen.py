import random
import pygame
import numpy as np

from Box2D import b2Vec2
from Box2D.b2 import world, polygonShape

from edu.vsb.viz.collision_handler import collision_handler
from edu.vsb.viz.obstacles.object_meta import object_meta, get_color_for_code
from edu.constants import STATE_H
from edu.constants import STATE_W
from edu.constants import STATE_PPM

pygame.display.set_caption('SkippingStones')


class viz_screen:
    def __init__(self):
        self.ppm = STATE_PPM  # pixels per meter, make it 1 when training
        self.target_fps = 20
        self.time_step = 1.0 / self.target_fps
        self.screen_width, self.screen_height = STATE_W, STATE_H # make it 32, 24 while training
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        self.clock = pygame.time.Clock()
        self.world = world(gravity=(0, 0), contactListener=collision_handler(self), doSleep=False)

        self.agent_target_pair = []  # agent is at index 0, target is at 1
        self.dynamic_obstacle_list = []
        self.static_obstacle_list = self.initialise_walls()

        self.reached_target = False
        self.collision_detected = False

    def reset_screen(self):
        self.clock = pygame.time.Clock()
        self.world = world(gravity=(0, 0), contactListener=collision_handler(self), doSleep=False)

        self.agent_target_pair = []  # agent is at index 0, target is at 1
        self.dynamic_obstacle_list = []
        self.static_obstacle_list = self.initialise_walls()
        self.reached_target = False
        self.collision_detected = False

    def add_agent_and_target(self, agent_at_pos, target_at_pos):
        self.agent_target_pair.clear()
        agent_metadata = object_meta(200)
        target_metadata = object_meta(300)

        agent = self.world.CreateDynamicBody(position=(agent_at_pos[0], agent_at_pos[1]))
        agent.CreatePolygonFixture(box=(0.5, 0.5), density=0.1, friction=0.1, restitution=1)

        agent.userData = agent_metadata
        self.agent_target_pair.append(agent)

        target = self.world.CreateStaticBody(position=(target_at_pos[0], target_at_pos[1]),
                                             shapes=polygonShape(box=(0.5, 0.5)))
        target.userData = target_metadata
        self.agent_target_pair.append(target)

        return agent, target

    def update_agent_position(self, update_step):
        agent_position = self.agent_target_pair[0].position
        f_x = update_step[0].item()
        f_y = update_step[1].item()
        applied_force = b2Vec2(f_x, f_y)
        self.agent_target_pair[0].ApplyLinearImpulse(impulse=applied_force,
                                                     point=b2Vec2(agent_position[0], agent_position[1]),
                                                     wake=True)

    def get_agent_target_distance(self):
        position_agent = self.agent_target_pair[0].position
        position_target = self.agent_target_pair[1].position
        position_agent = np.array((position_agent[0], position_agent[1]))
        position_target = np.array((position_target[0], position_target[1]))

        dist = np.linalg.norm(position_agent - position_target)
        return dist

    def get_dynamic_obstacle_states(self):
        ret_array = np.array([])
        for obstacle in self.dynamic_obstacle_list:
            obs_list = np.array([obstacle.position[0], obstacle.position[1], obstacle.angle])
            ret_array = np.concatenate((ret_array, obs_list), axis=None)
        return ret_array

    def add_static_obstacles(self, static_obstacles):
        self.static_obstacle_list.append(static_obstacles)

    def add_dynamic_obstacles(self, dynamic_obstacle_tuple):
        object_metadata = object_meta(500)
        for (pos_x, pos_y, angle) in dynamic_obstacle_tuple:
            temp_body = self.world.CreateDynamicBody(position=(pos_x, pos_y), angle=angle)
            temp_body.CreatePolygonFixture(box=(1, 1), density=1, friction=0.1, restitution=1)
            temp_body.userData = object_metadata
            self.dynamic_obstacle_list.append(temp_body)

    def apply_random_impulse(self):
        for body in self.dynamic_obstacle_list:
            impulse_x = random.random() * 15
            impulse_y = random.random() * 15

            axis_x = random.random() * 20
            axis_y = random.random() * 30
            body.ApplyLinearImpulse(impulse=(impulse_x, impulse_y), point=(axis_x, axis_y), wake=True)

    def initialise_walls(self):
        object_metadata = object_meta(100)
        left_wall = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=polygonShape(box=(1, 24)),
        )
        bottom_wall = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=polygonShape(box=(32, 1)),
        )
        right_wall = self.world.CreateStaticBody(
            position=(32, 0),
            shapes=polygonShape(box=(1, 24)),
        )
        top_wall = self.world.CreateStaticBody(
            position=(15, 24),
            shapes=polygonShape(box=(24, 1)),
        )
        left_wall.userData = object_metadata
        bottom_wall.userData = object_metadata
        right_wall.userData = object_metadata
        top_wall.userData = object_metadata

        return [left_wall, bottom_wall, right_wall, top_wall]

    def run_world(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0, 0))
            # Draw the world
            for body in self.static_obstacle_list:
                # The body gives us the position and angle of its shapes
                for fixture in body.fixtures:
                    shape = fixture.shape
                    if shape is not None:
                        vertices = [(body.transform * v) * self.ppm for v in shape.vertices]
                        vertices = [(v[0], self.screen_height - v[1]) for v in vertices]
                        pygame.draw.polygon(self.screen, self.get_color_for_object(body), vertices)

            for body in self.dynamic_obstacle_list:
                # The body gives us the position and angle of its shapes
                for fixture in body.fixtures:
                    shape = fixture.shape
                    if shape is not None:
                        vertices = [(body.transform * v) * self.ppm for v in shape.vertices]
                        vertices = [(v[0], self.screen_height - v[1]) for v in vertices]
                        pygame.draw.polygon(self.screen, self.get_color_for_object(body), vertices)
                    # pygame.draw.polygon(self.screen, self.colors[body.type], vertices)

            for body in self.agent_target_pair:
                # The body gives us the position and angle of its shapes
                for fixture in body.fixtures:
                    shape = fixture.shape
                    if shape is not None:
                        vertices = [(body.transform * v) * self.ppm for v in shape.vertices]
                        vertices = [(v[0], self.screen_height - v[1]) for v in vertices]
                        pygame.draw.polygon(self.screen, self.get_color_for_object(body), vertices)
                        # pygame.draw.polygon(self.screen, self.colors[body.type], vertices)

            self.world.Step(self.time_step, 10, 10)
            # Flip the screen and try to keep at the target FPS
            pygame.display.flip()
            self.get_image()
            self.clock.tick(self.target_fps)

    def get_color_for_object(self, box_object):
        return get_color_for_code(box_object.userData.get_obj_code())

    def get_image(self):
        pixels_3d = pygame.surfarray.array3d(self.screen)
        return pixels_3d

    def get_state(self):
        """ static_obstacle_pos, static_obstacle_dim, static_obstacle_pos, dyn_obstacle_pos_1, dyn_obstacle_pos_2,
        dyn_obstacle_pos_3, agent_pos, target_pos """

        pixels_3d = pygame.surfarray.array3d(self.screen)
        return pixels_3d

    def get_flags_done_collision(self):
        return self.reached_target, self.collision_detected

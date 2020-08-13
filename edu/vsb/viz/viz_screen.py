import random
import pygame
import numpy as np

from Box2D import b2Vec2
from Box2D.b2 import world, polygonShape, staticBody, dynamicBody

from edu.vsb.viz.collision_handler import collision_handler

pygame.display.set_caption('SkippingStones')


class viz_screen:
    def __init__(self):
        self.ppm = 20.0  # pixels per meter
        self.target_fps = 60
        self.time_step = 1.0 / self.target_fps
        self.screen_width, self.screen_height = 640, 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        self.clock = pygame.time.Clock()
        self.world = world(gravity=(0, 0), contactListener=collision_handler(), doSleep=False)

        self.agent_target_pair = []  # agent is at index 0, target is at 1
        self.dynamic_obstacle_list = []
        self.static_obstacle_list = self.initialise_walls()

        self.colors = {
            staticBody: (255, 168, 255, 255),
            dynamicBody: (127, 127, 255, 255)
        }

        self.reached_target = False
        self.collision_detected = False

    def reset_screen(self):
        self.clock = pygame.time.Clock()
        self.world = world(gravity=(0, 0), contactListener=collision_handler(), doSleep=False)

        self.agent_target_pair = []  # agent is at index 0, target is at 1
        self.dynamic_obstacle_list = []
        self.static_obstacle_list = self.initialise_walls()
        self.reached_target = False
        self.collision_detected = False

    def add_agent_and_target(self, agent_at_pos, target_at_pos):
        self.agent_target_pair.clear()

        agent = self.world.CreateStaticBody(position=(agent_at_pos[0], agent_at_pos[1]),
                                            shapes=polygonShape(box=(0.5, 0.5)))
        self.agent_target_pair.append(agent)

        target = self.world.CreateStaticBody(position=(target_at_pos[0], target_at_pos[1]),
                                             shapes=polygonShape(box=(0.5, 0.5)))
        self.agent_target_pair.append(target)

        return agent, target

    def update_agent_position(self, update_step):
        position = self.agent_target_pair[0].position
        self.agent_target_pair[0].position = b2Vec2(position[0] + update_step[0], position[1] - update_step[1])

    def get_agent_target_distance(self):
        position_agent = self.agent_target_pair[0].position
        position_target = self.agent_target_pair[1].position
        position_agent = np.array((position_agent[0], position_agent[1]))
        position_target = np.array((position_target[0], position_target[1]))

        dist = np.linalg.norm(position_agent - position_target)
        return dist

    def add_static_obstacles(self, static_obstacles):
        self.static_obstacle_list.append(static_obstacles)

    def add_dynamic_obstacles(self, dynamic_obstacle_tuple):
        for (pos_x, pos_y, angle) in dynamic_obstacle_tuple:
            temp_body = self.world.CreateDynamicBody(position=(pos_x, pos_y), angle=angle)
            temp_body.CreatePolygonFixture(box=(1, 1), density=1, friction=0.1, restitution=1)
            self.dynamic_obstacle_list.append(temp_body)

    def apply_impulse(self):
        for body in self.dynamic_obstacle_list:
            impulse_x = random.random() * 15
            impulse_y = random.random() * 15
            body.ApplyLinearImpulse(impulse=(impulse_x, impulse_y), point=(10, 15), wake=True)

    def initialise_walls(self):
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
                    vertices = [(body.transform * v) * self.ppm for v in shape.vertices]
                    vertices = [(v[0], self.screen_height - v[1]) for v in vertices]
                    pygame.draw.polygon(self.screen, self.colors[body.type], vertices)

            for body in self.dynamic_obstacle_list:
                # The body gives us the position and angle of its shapes
                for fixture in body.fixtures:
                    shape = fixture.shape
                    vertices = [(body.transform * v) * self.ppm for v in shape.vertices]
                    vertices = [(v[0], self.screen_height - v[1]) for v in vertices]
                    pygame.draw.polygon(self.screen, self.colors[body.type], vertices)

            for body in self.agent_target_pair:
                # The body gives us the position and angle of its shapes
                for fixture in body.fixtures:
                    shape = fixture.shape
                    vertices = [(body.transform * v) * self.ppm for v in shape.vertices]
                    vertices = [(v[0], self.screen_height - v[1]) for v in vertices]
                    pygame.draw.polygon(self.screen, self.colors[body.type], vertices)

            self.world.Step(self.time_step, 10, 10)
            # Flip the screen and try to keep at the target FPS
            pygame.display.flip()
            self.clock.tick(self.target_fps)

    def begin_contact(self, contact):
        fixture_a = contact.fixtureA
        fixture_b = contact.fixtureB

        body_a, body_b = fixture_a.body, fixture_b.body

import random
import pygame
from Box2D import b2Vec2
from Box2D.b2 import world, polygonShape, staticBody, dynamicBody

pygame.display.set_caption('SkippingStones')


class viz_screen:
    def __init__(self):
        self.ppm = 20.0  # pixels per meter
        self.target_fps = 60
        self.time_step = 1.0 / self.target_fps
        self.screen_width, self.screen_height = 640, 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        self.clock = pygame.time.Clock()
        self.world = world(gravity=(0, 0), doSleep=False)

        self.agent_target_pair = []  # agent is at index 0, target is at 1
        self.dynamic_obstacle_list = []
        self.static_obstacle_list = self.initialise_walls()

        self.colors = {
            staticBody: (255, 168, 255, 255),
            dynamicBody: (127, 127, 255, 255),
        }
        self.add_agent([13, 13])

        self.reached_target = False
        self.collision_detected = False

    def add_agent(self, at_pos):
        agent = self.world.CreateStaticBody(position=(at_pos[0], at_pos[1]),
                                            shapes=polygonShape(box=(0.5, 0.5)))
        self.agent_target_pair.append(agent)
        return agent

    def add_target(self, at_pos):
        target = self.world.CreateStaticBody(position=(at_pos[0], at_pos[1]),
                                             shapes=polygonShape(box=(0.5, 0.5)))
        self.agent_target_pair.append(target)
        return target

    def get_agent_target_distance(self):
        distance = 2     # todo: implement this
        return distance

    def update_agent_position(self, update_step):
        position = self.agent_target_pair[0].position
        self.agent_target_pair[0].position = b2Vec2(position[0] + update_step[0], position[1] - update_step[1])
        print(position)

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
            shapes=polygonShape(box=(1, 50)),
        )
        bottom_wall = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=polygonShape(box=(50, 1)),
        )
        right_wall = self.world.CreateStaticBody(
            position=(32, 10),
            shapes=polygonShape(box=(1, 20)),
        )
        top_wall = self.world.CreateStaticBody(
            position=(15, 24),
            shapes=polygonShape(box=(20, 1)),
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
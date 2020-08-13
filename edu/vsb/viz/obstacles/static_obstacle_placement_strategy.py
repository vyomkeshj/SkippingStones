import random


# todo: block the los between agent and target with static blocks
class static_obstacle_placement_strategy:
    def __init__(self, bounds=(3, 3, 20, 20)):
        self.num_obstacles = random.randint(2, 6)
        self.generation_bounds = bounds
        self.obstacle_min_size = 0.25
        self.obstacle_max_size = 0.5
        self.mean_spacing = 4

    def get_obstacles(self, agent_init_pos, target_init_pos):
        # print("generating obstakles to takle babe")
        width_of_agent = 1
        ret_list = []

        for i in range(self.num_obstacles):
            x = random.uniform(min(agent_init_pos[0], target_init_pos[0]) + width_of_agent,
                               max(agent_init_pos[0], target_init_pos[0]) - width_of_agent)

            y = None
            y1 = agent_init_pos[1]
            y2 = target_init_pos[1]
            if abs(y1 - y2) < 1:
                y_choice = random.randint(0, 1)
                if (y_choice == 1):
                    y = y1
                else:
                    y = y2

            else:
                y = random.uniform(min(y1, y2) + width_of_agent, max(y1, y2) - width_of_agent)
            l = random.uniform(self.obstacle_min_size, self.obstacle_max_size)
            theta = random.uniform(0, 90)
            # print(x, y, l, theta)
            ret_list.append([(x, y), l, theta])
        # print(ret_list)
        return (ret_list)

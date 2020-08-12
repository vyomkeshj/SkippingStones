

# todo: block the los between agent and target with static blocks
class static_obstacle_placement_strategy:
    def __init__(self, num_obstacle_range, actor_target_generator):
        self.obstacle_count_range = num_obstacle_range
        self.actor_target_generator = actor_target_generator


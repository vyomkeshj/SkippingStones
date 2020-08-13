standard_codes = {
    100: "walls",
    200: "agent",
    300: "target",
    400: "static_obstacle",
    500: "dynamic_obstacle"
}
standard_colors = {
    "walls": (255, 168, 255, 255),
    "agent": (127, 127, 255, 255),
    "target": (255, 0, 0, 255),
    "static_obstacle": (123, 168, 0, 255),
    "dynamic_obstacle": (123, 255, 0, 255)
}


def get_color_for_code(code):
    return standard_colors.get(standard_codes.get(code))


class object_meta:

    def __init__(self, object_code):
        self.object_code = object_code

    def get_obj_code(self):
        return self.object_code


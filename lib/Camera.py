import math

class Camera:
    def __init__(self, x, y, direction, canvas):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.direction = direction  # "front", "back", "right", or "left"
        self.vision_distance = 50

    def get_distance_to_edge(self, car_direction, x, y):
        self.x = x
        self.y = y
        # Define a tolerance distance to consider the car not colliding with the edge
        tolerance_distance = 2

        angle_radians = math.radians(car_direction)  # Convert car direction angle to radians

        if self.direction == "front":
            return self._get_distance_in_direction(math.cos(angle_radians), -math.sin(angle_radians), tolerance_distance)
        elif self.direction == "back":
            return self._get_distance_in_direction(-math.cos(angle_radians), math.sin(angle_radians), tolerance_distance)
        elif self.direction == "right":
            return self._get_distance_in_direction(math.sin(angle_radians), math.cos(angle_radians), tolerance_distance)
        elif self.direction == "left":
            return self._get_distance_in_direction(-math.sin(angle_radians), -math.cos(angle_radians), tolerance_distance)
        else:
            raise ValueError("Invalid direction for the camera")

    def _get_distance_in_direction(self, dx, dy, tolerance_distance):
        x, y = self.x, self.y
        distance = 0

        while distance <= self.vision_distance:
            if not self._is_object_on_position(x, y):
                return distance - tolerance_distance
            x += dx
            y += dy
            distance += 1

        return -1

    def _is_object_on_position(self, x, y):
        # Get all objects that overlap the (x, y) position
        overlapping_objects = self.canvas.find_overlapping(x, y, x, y)

        # Filter objects that are tagged with "street"
        overlapping_street_objects = [
            obj_id for obj_id in overlapping_objects if "street" in self.canvas.gettags(obj_id)
        ]

        # Check if there are any overlapping street objects
        return len(overlapping_street_objects) > 0

    def is_goal_in_range(self, car_direction, level):
        goal_x, goal_y = level[-1]["X"], level[-1]["Y"]
        distance_to_goal = ((goal_x - self.x) ** 2 + (goal_y - self.y) ** 2) ** 0.5
        if distance_to_goal <= self.vision_distance:
            return self._is_goal_visible(car_direction, goal_x, goal_y)
        else:
            return False

    def _is_goal_visible(self, car_direction, goal_x, goal_y):
        angle_radians = math.radians(car_direction)  # Convert car direction angle to radians
        dx = goal_x - self.x
        dy = goal_y - self.y
        distance_to_goal = math.sqrt(dx ** 2 + dy ** 2)

        if distance_to_goal <= self.vision_distance:
            angle_to_goal_radians = math.atan2(dy, dx)
            relative_angle_radians = angle_to_goal_radians - angle_radians

            # Normalize the relative angle to be within the range (-pi, pi)
            while relative_angle_radians <= -math.pi:
                relative_angle_radians += 2 * math.pi
            while relative_angle_radians > math.pi:
                relative_angle_radians -= 2 * math.pi

            # Goal is within 45 degrees field of view and has "goal" tag
            return abs(relative_angle_radians) < math.pi / 4 and self._has_goal_tag(goal_x, goal_y)
        else:
            return False

    def _has_goal_tag(self, x, y):
        # Get all objects that overlap the (x, y) position
        overlapping_objects = self.canvas.find_overlapping(x, y, x, y)

        # Check if any of the overlapping objects have the "goal" tag
        for obj_id in overlapping_objects:
            if "goal" in self.canvas.gettags(obj_id):
                return True

        return False

    def calculate_distance_to_goal(self, car_direction, level, x, y):
        self.x = x
        self.y = y
        goal_x, goal_y = level[-1]["X"], level[-1]["Y"]
        distance_to_goal = ((goal_x - self.x) ** 2 + (goal_y - self.y) ** 2) ** 0.5
        if distance_to_goal <= self.vision_distance:
            if self._is_goal_visible(car_direction, goal_x, goal_y):
                return distance_to_goal
            else:
                return -1
        else:
            return -1
import math
from .Camera import Camera

class Car:
    def __init__(self, canvas, x, y, initial_direction, distance):
        self.canvas = canvas
        self.direction = initial_direction
        length = 25 #car length
        breadth = 10 #car breadth
        angle_radians = math.radians(initial_direction)
        half_length = length / 2
        half_breadth = breadth / 2
        points = []
        num_points = 100  # Increase this value for a smoother ellipse
        for i in range(num_points):
            t = 2 * math.pi * i / num_points
            x0 = x + half_length * math.cos(t) * math.cos(angle_radians) - half_breadth * math.sin(t) * math.sin(angle_radians)
            y0 = y + half_length * math.cos(t) * math.sin(angle_radians) + half_breadth * math.sin(t) * math.cos(angle_radians)
            points.append((x0, y0))
        # Draw the oriented ellipse (as the car) using the calculated points
        self.car_id =  canvas.create_polygon(points, fill="red", outline="black", width=1)
        #Calculate endpoints of the line showing the direction of the car
        self.line_length = 15
        line_end_x = x + self.line_length * math.cos(angle_radians)
        line_end_y = y + self.line_length * math.sin(angle_radians)

        # Draw the line starting from the center of the car
        self.direction_line = self.canvas.create_line(x, y, line_end_x, line_end_y, fill="blue", width=2)


        # Create camera objects for the car
        self.cameras = [
            Camera(x, y, "front", self.canvas),
            Camera(x, y, "back", self.canvas),
            Camera(x, y, "right", self.canvas),
            Camera(x, y, "left", self.canvas)
        ]

        self.alive = True  # Initially, the car is alive
        self.distance = distance #Distance to finish over streets
        self.previous = (x,y) #Save most recent crossed street startpoint

    #Set point of next street for the car to reach
    def setNext(self, next_x, next_y):
        self.distance -= ((next_x - self.previous[0]) ** 2 + (next_y - self.previous[1]) ** 2) ** 0.5
        self.next_x = next_x
        self.next_y = next_y

    #Get point of next street for the car to reach
    def getNext(self):
        return (self.next_x, self.next_y)

    def setDistance(self, distance):
        self.distance = distance

    def getDistance(self):
        return self.distance
        
    #Returns distance to the point of the next street for the car to reach
    def getStreetDistance(self):
        x, y = self.canvas.coords(self.car_id)[0], self.canvas.coords(self.car_id)[1]
        return ((self.next_x - x) ** 2 + (self.next_y - y) ** 2) ** 0.5

    def combined_distance(self):
        return (self.getDistance(), self.getStreetDistance())
    
    def move(self, dx, dy):
        x, y = self.canvas.coords(self.car_id)[0]+dx, self.canvas.coords(self.car_id)[1]+dy
        self.redraw_car(x, y)
        # Update the coordinates of the forward line to point in the new direction
        x1, y1 = x + self.line_length * math.cos(math.radians(self.direction)), y + self.line_length * math.sin(math.radians(self.direction))
        self.canvas.coords(self.direction_line, x, y, x1, y1)

    def update(self, brain, level):
        if not self.alive:
            return False  # If the car is dead, return False immediately

        car_x, car_y = self.canvas.coords(self.car_id)[0], self.canvas.coords(self.car_id)[1]

        # Get the camera values
        distances = [camera.get_distance_to_edge(self.direction, car_x, car_y) for camera in self.cameras]
        goal_distances = [camera.calculate_distance_to_goal(self.direction, level, car_x, car_y) for camera in self.cameras]
        # Check if the car hits the edge
        hit_edge = (distances[0] <= 13 and distances[0] != -1) or (distances[1] <= 13 and distances[1] != -1) or (distances[2] <= 6 and distances[2] != -1) or (distances[3] <= 6 and distances[3] != -1)
        if hit_edge:
            self.alive = False
            self.canvas.delete(self.direction_line) # Delete the direction line
            self.canvas.itemconfig(self.car_id, fill="black")  # Change the car to black
            return False

        # Calculate the turn angle
        turn_angle = brain.calculate_turn_angle(distances, goal_distances)
        self.direction += turn_angle

        move_distance = brain.calculate_move(distances, goal_distances)
        # Calculate the x and y components of the move distance based on the car's current direction
        direction_angle_rad = math.radians(self.direction)
        dx = move_distance * math.cos(direction_angle_rad)
        dy = move_distance * math.sin(direction_angle_rad)
        self.move(dx, dy)

        return True

    def redraw_car(self, x, y):
        length = 25 #car length
        breadth = 10 #car breadth
        angle_radians = math.radians(self.direction)
        half_length = length / 2
        half_breadth = breadth / 2
        points = []
        num_points = 100  # Increase this value for a smoother ellipse
        for i in range(num_points):
            t = 2 * math.pi * i / num_points
            x0 = x + half_length * math.cos(t) * math.cos(angle_radians) - half_breadth * math.sin(t) * math.sin(angle_radians)
            y0 = y + half_length * math.cos(t) * math.sin(angle_radians) + half_breadth * math.sin(t) * math.cos(angle_radians)
            points.append((x0, y0))
        # Draw the oriented ellipse (as the car) using the calculated points
        self.canvas.delete(self.car_id)
        self.car_id = self.canvas.create_polygon(points, fill="red", outline="black", width=1)
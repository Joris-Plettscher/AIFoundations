import tkinter as tk
import json
import os
from lib.Car import Car
import math
from math import atan2, degrees
import random
from options.Iteration import Iteration
import time

class Simulation:
    def __init__(self, root, car_number=10):
        self.root = root
        self.car_number = car_number  # Number of cars to simulate
        self.label = tk.Label(root, text="Enter the index of the level to simulate:")
        self.label.pack()

        self.index_entry = tk.Entry(root)
        self.index_entry.pack()

        self.display_button = tk.Button(root, text="Simulate Level", command=self.simulate_level)
        self.display_button.pack()

        self.canvas = tk.Canvas(root, bg="green", width=root.winfo_screenwidth(), height=root.winfo_screenheight()-50) # Reduce 50px to accommodate for the taskbar
        self.canvas.pack()

        self.levels = self.load_levels()

    def simulate_level(self):
        try:
            index = int(self.index_entry.get())
            if 0 <= index < len(self.levels):
                self.canvas.delete("all")
                level = self.levels[index]
                self.draw_level(level)

                #Calculate initial distance to finish (Add distances of all points of the level)
                total_distance = 0
                for i in range(len(level) - 1):
                    x1, y1 = level[i]["X"], level[i]["Y"]
                    x2, y2 = level[i + 1]["X"], level[i + 1]["Y"]
                    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    total_distance += distance
                # If the level has at least two points, set the initial direction as the angle between the first two points
                if len(level) >= 2:
                    first_x, first_y = level[0]["X"], level[0]["Y"]
                    second_x, second_y = level[1]["X"], level[1]["Y"]
                    angle_deg = math.degrees(math.atan2(second_y - first_y, second_x - first_x))
                else:
                    first_x, first_y = random.uniform(50, 750), random.uniform(50, 550)
                    angle_deg = 0  # If there's only one point, set the initial angle to 0 degrees
                self.cars = []  # List to store the cars
                for _ in range(self.car_number):
                    self.cars.append(self.place_car(first_x, first_y, angle_deg, total_distance))
                #Set next point of next street to reach for every car on the starting point of the second street
                for car in self.cars:
                    car.setNext(level[1]["X"], level[1]["Y"])
                nextStreet = [1] * self.car_number #Stores index of next street of every car
                # Start the iteration and keep running until it returns False
                iteration = Iteration(self.cars, self.car_number, level)
                while iteration.run():
                    self.root.update_idletasks()
                    time.sleep(0.000001)
                    for car in self.cars:
                        car_idx = self.cars.index(car)
                        #Adjust distances of cars if they've reached a new street (within certain radius of street start point)
                        car_x, car_y = self.canvas.coords(car.car_id)[0], self.canvas.coords(car.car_id)[1]
                        if(self.is_within_radius((car_x, car_y), (car.getNext()))):
                            nextStreet[car_idx]+=1
                            car_next = nextStreet[car_idx]
                            car.setNext(level[car_next]["X"], level[car_next]["Y"])
                        #Replace dead cars
                        if(not car.alive):
                            self.cars[car_idx] = self.place_car(first_x, first_y, angle_deg, total_distance)
                            new_car = self.cars[car_idx]
                            new_car.setNext(level[1]["X"], level[1]["Y"])
                            nextStreet[car_idx] = 1
                            iteration.resetBrain(car_idx)
            else:
                self.canvas.delete("all")
                self.canvas.create_text(
                    10, 10, anchor="nw", text="The level of the given index doesn't exist.", fill="black", font=("Helvetica", 14)
                )
        except ValueError:
            self.canvas.delete("all")
            self.canvas.create_text(
                10, 10, anchor="nw", text="Invalid index. Please enter a valid integer.", fill="black", font=("Helvetica", 14)
            )

    def load_levels(self):
        try:
            # Load existing levels from the "levels.json" file
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res", "levels.json")
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                return data.get("Levels", [])
        except FileNotFoundError:
            # If the file doesn't exist, return an empty list
            return []
        
    def draw_level(self, level):
        for i in range(1, len(level)):
            prev_x, prev_y = level[i - 1]["X"], level[i - 1]["Y"]
            x, y = level[i]["X"], level[i]["Y"]
            self.canvas.create_line(prev_x, prev_y, x, y, fill="dark gray", width=50, capstyle='round', joinstyle='round', tags='street')
        # Draw a checkered black and white rectangle at the last point of the level
        last_x, last_y = level[-1]["X"], level[-1]["Y"]
        size = 25
        for i in range(-size, size, 10):
            for j in range(-size, size, 10):
                color = "black" if (i + j) % 20 == 0 else "white"
                self.canvas.create_rectangle(last_x + i, last_y + j, last_x + i + 10, last_y + j + 10, fill=color)
        self.canvas.create_rectangle(last_x - size, last_y - size, last_x + size, last_y + size, outline="black", tags='goal')

    def place_car(self, x, y, initial_direction, distance):
        return Car(self.canvas, x, y, initial_direction, distance)

    def is_within_radius(self, point1, point2, radius=25):
        # Calculate the distance between the two points using the Euclidean distance formula
        distance = ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5

        # Check if the distance is less than or equal to the radius
        return distance <= radius

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulation")

    # Calculate the screen height above the taskbar (subtract 50 pixels for the taskbar)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() - 50

    # Set the window size and position to cover the screen above the taskbar
    root.geometry("{0}x{1}+0+0".format(screen_width, screen_height))
    
    app = Simulation(root)

    def close_app():
        root.destroy()

    # Create a close button
    close_button = tk.Button(root, text="Close", command=close_app)
    close_button.pack()

    root.mainloop()

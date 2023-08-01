from .ExampleBrain import ExampleBrain

class IterationExample:
    def __init__(self, cars, number_of_cars, level, tolerance = 2):
        self.level = level
        self.cars = cars
        self.brains = [ExampleBrain() for _ in range(number_of_cars)]
        self.brain = self.brains[0] # No best brain yet
        self.best_distance = (-1,-1) # No best distance yet
        self.number_of_cars = number_of_cars
        self.current_deaths = 0
        self.tolerance = tolerance

    def run(self):
        for i in range(0,self.number_of_cars):
            car = self.cars[i]
            brain = self.brains[i]
            distances = [-1] * self.number_of_cars
            streetDistances = [-1] * self.number_of_cars
            if not car.update(brain, self.level):
                #Removing last movement and turn of current brain
                brain.movements = brain.movements[:-1]
                brain.turns = brain.turns[:-1]
                self.current_deaths += 1
                # Check if current best brain not working -> remove last 3 steps if possible
                if(self.current_deaths >= self.number_of_cars * self.tolerance):
                    try:
                        self.brain.movements = self.brain.movements[:-3]
                    except Exception:
                        self.brain.movements = self.brain.movements[:-1]
                    try:
                        self.brain.turns = self.brain.turns[:-3]
                    except Exception:
                        self.brain.turns = self.brain.turns[:-1]
                    self.current_deaths = 0
            # Check if goal was reached by a car -> simulation ends
            for camera in car.cameras:
                goal_distance = camera.calculate_distance_to_goal(car.direction,self.level, car.canvas.coords(car.car_id)[0], car.canvas.coords(car.car_id)[1])
                if(goal_distance is None):
                    continue
                if(goal_distance <= 13 and goal_distance != -1): #If a car reached the goal -> end
                    self.brain = self.brains[i]
                    return False
        # Determine best brain
        car_with_lowest_distance = min(self.cars, key=lambda car: car.combined_distance())
        best_car_idx = self.cars.index(car_with_lowest_distance)
        lowest_distance = car_with_lowest_distance.combined_distance()
        #If best brain of current run is better than best brain -> modify best brain
        if (self.best_distance == (-1,-1)) or (lowest_distance[0] < self.best_distance[0]) or (lowest_distance[0] == self.best_distance[0] and lowest_distance[1] < self.best_distance[1]):
            self.brain = self.brains[best_car_idx].copy()
            self.best_distance = lowest_distance
            self.current_deaths = 0
        return True

    # Returns the brain to use for new cars
    def getBrain(self):
        brain = self.brain.copy()
        #Removing last move and turn for variance
        brain.movements = brain.movements[:-1]
        brain.turns = brain.turns[:-1]
        return brain

    def resetBrain(self, idx):
        self.brains[idx] = self.getBrain()

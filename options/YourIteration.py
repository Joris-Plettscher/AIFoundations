from .YourBrain import YourBrain

class YourIteration:
    def __init__(self, cars, number_of_cars, level):
        # Initialize your Iteration here

    def run(self):
        for i in range(0,self.number_of_cars):
            car = self.cars[i]
            brain = self.brains[i]
            if not car.update(brain, self.level):
                pass
            # Check if goal was reached by a car -> simulation ends
            for camera in car.cameras:
                goal_distance = camera.calculate_distance_to_goal(car.direction,self.level, car.canvas.coords(car.car_id)[0], car.canvas.coords(car.car_id)[1])
                if(goal_distance is None):
                    continue
                if(goal_distance <= 13 and goal_distance != -1): #If a car reached the goal -> end
                    self.brain = self.brains[i]
                    return False
        # Determine your best brain ...
        return True

    # Returns the brain to use for new cars
    def getBrain(self):
        return 

    def resetBrain(self, idx):
        self.brains[idx] = self.getBrain()

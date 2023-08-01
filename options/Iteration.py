#Import your Iteration implementation here:
from .IterationExample import IterationExample

class Iteration:
    def __init__(self, cars, number_of_cars, level):
        #Initialize your Iteration implementation here:
        # Param cars: List of Car objects
        # Param number_of_cars: Integer
        # Param level: List of starting points of the streets. Every starting point is a dictionary with a x and y value (coordinates)
        self.iter = IterationExample(cars, number_of_cars, level) 

    def run(self) -> bool:
        # This is the method which will be executed every step. 
        # You should update the cars here and you can set important variables for the next step
        # Return true if the simulation should continue, else return false (One option is to check if a car has reached the goal)
        return self.iter.run()

    def getBrain(self):
        #Return the brain which should be used for respawned cars (dead cars will be replaced with new ones)
        return self.iter.getBrain

    def resetBrain(self, idx):
        # Method to set the brain with index idx to a brain which should be used for new cars (eg. best performing brain)
        self.iter.resetBrain(idx)

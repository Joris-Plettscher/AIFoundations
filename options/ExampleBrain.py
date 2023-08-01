import random

class ExampleBrain:
    def __init__(self):
        self.movements = []  # List to store the movements (forward or backward)
        self.turns = []      # List to store the turns (angle degrees)
        self.current_turn = 0
        self.current_move = 0

    def calculate_turn_angle(self, distances, goal_in_range):
        if self.current_turn < len(self.turns):
            self.current_turn += 1
            return self.turns[self.current_turn-1]
        # Perform a random turn between -50 and 50 degrees
        turn_angle = random.randint(-50, 50)
        self.turns.append(turn_angle)  # Save the turn for tracking
        self.current_turn += 1
        return turn_angle

    def calculate_move(self, distances, goal_in_range):
        if self.current_move < len(self.movements):
            self.current_move += 1
            return self.movements[self.current_move-1]
        # Perform a random move between -10 and 10 units
        move_distance = random.randint(-1, 1)
        self.movements.append(move_distance)  # Save the movement for tracking
        self.current_move += 1
        return move_distance

    def copy(self):
        """
        Create a deep copy of the ExampleBrain instance.
        Returns:
            ExampleBrain: A new instance with the same movements and turns.
        """
        copied_brain = ExampleBrain()
        copied_brain.movements = self.movements
        copied_brain.turns = self.turns
        return copied_brain

import tkinter as tk
import json
import os

class LevelDesigner:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, bg="green", width=root.winfo_screenwidth(), height=root.winfo_screenheight()-50) # Reduce 50px to accommodate for the taskbar
        self.canvas.pack()

        self.start_x, self.start_y = None, None
        self.prev_x, self.prev_y = None, None
        self.current_line = []  # List to store the points of the current line
        self.levels = self.load_levels()  # List to store all drawn levels

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Add the label for the instruction text
        self.instruction_label = tk.Label(root, text="Press 's' to save the level", fg="black")
        self.instruction_label.place(x=10, y=10)  # Position the label at the top-left corner

        # Bind the 's' key press event to save the level
        root.bind("<s>", self.save_level)

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        if self.start_x is None:
            # Set the starting point for the first line
            self.start_x, self.start_y = x, y
            self.prev_x, self.prev_y = x, y
        else:
            # Draw the line from the previous point to the current point
            line_id = self.canvas.create_line(self.prev_x, self.prev_y, x, y, fill="dark gray", width=5)
            self.current_line.extend([{"X": self.prev_x, "Y": self.prev_y}])
            self.prev_x, self.prev_y = x, y

    def save_level(self, event):
        if self.start_x is not None and self.start_y is not None and self.prev_x is not None and self.prev_y is not None:
            # Save the last point of the current line
            self.current_line.extend([{"X": self.prev_x, "Y": self.prev_y}])
            # Add the current level to the list of levels
            self.levels.append(self.current_line)
            self.current_line = []  # Reset the current line points

            # Save the levels to JSON format
            data = {"Levels": self.levels}

            # Save the levels to the "levels.json" file
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "res", "levels.json")
            with open(file_path, "w") as json_file:
                json.dump(data, json_file, indent=2)

            print("Level saved!")
            # Clear the drawn lines after saving
            self.canvas.delete("all")
            self.start_x, self.start_y = None, None
            self.prev_x, self.prev_y = None, None

    def load_levels(self):
        try:
            # Load existing levels from the "levels.json" file
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "res", "levels.json")
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                return data.get("Levels", [])
        except FileNotFoundError:
            # If the file doesn't exist, create an empty structure
            return []

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Line Drawer")

    # Calculate the screen height above the taskbar (subtract 50 pixels for the taskbar)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() - 50

    # Set the window size and position to cover the screen above the taskbar
    root.geometry("{0}x{1}+0+0".format(screen_width, screen_height))
    
    app = LevelDesigner(root)

    def close_app():
        root.destroy()

    # Create a close button
    close_button = tk.Button(root, text="Close", command=close_app)
    close_button.pack()

    root.mainloop()

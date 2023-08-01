import tkinter as tk
import json
import os

class LevelViewer:
    def __init__(self, root):
        self.root = root
        self.label = tk.Label(root, text="Enter the index of the level to display:")
        self.label.pack()

        self.index_entry = tk.Entry(root)
        self.index_entry.pack()

        self.display_button = tk.Button(root, text="Display Level", command=self.display_level)
        self.display_button.pack()

        self.canvas = tk.Canvas(root, bg="green", width=root.winfo_screenwidth(), height=root.winfo_screenheight()-50) # Reduce 50px to accommodate for the taskbar
        self.canvas.pack()

        self.levels = self.load_levels()

    def display_level(self):
        try:
            index = int(self.index_entry.get())
            if index >= 0 and index < len(self.levels):
                self.canvas.delete("all")
                level = self.levels[index]
                self.draw_level(level)
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
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "res", "levels.json")
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
            self.canvas.create_line(prev_x, prev_y, x, y, fill="dark gray", width=50, capstyle='round', joinstyle='round')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Display Level")

    # Calculate the screen height above the taskbar (subtract 50 pixels for the taskbar)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() - 50

    # Set the window size and position to cover the screen above the taskbar
    root.geometry("{0}x{1}+0+0".format(screen_width, screen_height))
    
    app = LevelViewer(root)

    def close_app():
        root.destroy()

    # Create a close button
    close_button = tk.Button(root, text="Close", command=close_app)
    close_button.pack()

    root.mainloop()

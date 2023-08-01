import tkinter as tk
import json
import os

class LevelRemover:
    def __init__(self, root):
        self.root = root
        self.label = tk.Label(root, text="Enter the index of the level to remove:")
        self.label.pack()

        self.index_entry = tk.Entry(root)
        self.index_entry.pack()

        self.remove_button = tk.Button(root, text="Remove Level", command=self.remove_level)
        self.remove_button.pack()

        self.result_label = tk.Label(root, text="", fg="red")
        self.result_label.pack()

    def remove_level(self):
        try:
            index = int(self.index_entry.get())
            levels = self.load_levels()
            if index >= 0 and index < len(levels):
                levels.pop(index)
                self.save_levels(levels)
                self.result_label.config(text="Level at index {} has been removed.".format(index), fg="black")
            else:
                self.result_label.config(text="The level of the given index doesn't exist.", fg="red")
        except ValueError:
            self.result_label.config(text="Invalid index. Please enter a valid integer.", fg="red")

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

    def save_levels(self, levels):
        # Save the updated levels to the "levels.json" file
        data = {"Levels": levels}
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "res", "levels.json")
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Remove Level")

    app = LevelRemover(root)

    root.mainloop()

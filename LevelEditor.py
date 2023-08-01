import tkinter as tk
from lib.LevelDesigner import LevelDesigner
from lib.LevelViewer import LevelViewer
from lib.LevelRemover import LevelRemover

class LevelEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Level Editor")

        # Set the width and height for the buttons to make them bigger
        button_width = 100
        button_height = 3
        
        self.designer_button = tk.Button(root, text="Level Designer", command=self.open_designer, width=button_width, height=button_height)
        self.designer_button.pack()

        self.viewer_button = tk.Button(root, text="Level Viewer", command=self.open_viewer, width=button_width, height=button_height)
        self.viewer_button.pack()

        self.remover_button = tk.Button(root, text="Level Remover", command=self.open_remover, width=button_width, height=button_height)
        self.remover_button.pack()

    def open_designer(self):
        designer_window = tk.Toplevel(self.root)
        designer_app = LevelDesigner(designer_window)

    def open_viewer(self):
        viewer_window = tk.Toplevel(self.root)
        viewer_app = LevelViewer(viewer_window)

    def open_remover(self):
        remover_window = tk.Toplevel(self.root)
        remover_app = LevelRemover(remover_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = LevelEditorApp(root)
    root.mainloop()

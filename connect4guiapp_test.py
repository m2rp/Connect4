#!/usr/bin/python3
import pathlib
import pygubu
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui_1.ui"


class Gui1App:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1")
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def human_button_click(self):
        print("Human button clicked")
        self.mainwindow.destroy()
        self.mainwindow = self.builder.get_object("toplevel2")
        self.run()
        
    def comp_button_click(self):
        print("Computer button clicked")


if __name__ == "__main__":
    app = Gui1App()
    app.run()

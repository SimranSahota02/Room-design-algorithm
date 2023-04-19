import tkinter as tk
import gui_frame as gu
import room_items as ri
import gui_grid as gi 

class room_doors(gu.gui_frame):

    rad_adding_item = None  # radio button for what the user is adding with a click
    addable_items = []
    btn_reset = None # reset the room layout to start again
    my_grid = None
    
    # show the radio buttons and reset button
    # show a grid the size of the room
    #  populate the grid with the contents of the room

    def __init__(self, parent, controller):

        super().__init__(
            parent, controller
        )  # call the constructor for the parent class (gui_frame)
        
        self.load_room_into_grid()

        fra_rhs = tk.Frame(self.mainframe)  
        fra_rhs.pack(side=tk.RIGHT, fill = tk.Y)

        tk.Label(fra_rhs, text="Select below then click in the grid to add", anchor=tk.CENTER).pack(
            side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        self.rad_adding_item = tk.IntVar()
        self.rb_door=tk.Radiobutton(fra_rhs, text="Door", variable=self.rad_adding_item, value=0)
        self.rb_door.pack(side = tk.TOP, anchor=tk.W, padx=2, pady=2)
        self.addable_items.append(ri.Door)

        self.rb_wall = tk.Radiobutton(fra_rhs, text="Wall", variable=self.rad_adding_item, value=1)
        self.rb_wall.pack(side = tk.TOP, anchor=tk.W, padx=2, pady=2)
        self.addable_items.append(ri.Wall)

        self.rb_none = tk.Radiobutton(fra_rhs, text="Nothing", variable=self.rad_adding_item, value=2)
        self.rb_none.pack(side = tk.TOP, anchor=tk.W, padx=2, pady=2)
        self.addable_items.append(None)
        





    def load_room_into_grid(self):
        # first, destroy the current grid (if it exists)
        if self.my_grid is not None:
            self.my_grid.destroy()

        self.my_grid = gi.Cell_Grid(self.mainframe, 
                    self.controller.base_room,
                    15,
                    self.rad_adding_item,
                    self.addable_items)

        self.my_grid.pack(side = tk.LEFT, fill = tk.BOTH, expand= tk.TRUE)


    def on_show_frame(self, event, arg):
        # fires when page is loaded
        self.set_title(
            "Set location of doors for: " + str(self.controller.get_room_name())
        )
        self.load_room_into_grid()




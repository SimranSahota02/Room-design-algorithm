import tkinter as tk
import python_array_test as rm
import room_items as ri
import PIL.ImageTk
import gui_frame as gu
import gui_grid as gi 

# Show the room grid
# Populate the grid with the furniture in the rooom grid
# switch between the available room grids


class show_room(gu.gui_frame):

    lbx_unused = None  # list of unused items in the current room design
    fra_design = None  # frame to hold the current room design
    current_design = -1  # which design to load from the available designs
    current_design_text = None  # to show the current design number in a label
    furniture_widgets = None  # holds the furniture items and imagesfor each placed furniture item, if don't keep them they get destroyed
    my_grid = None
    # 3x3 grid for the main frame
    # inside the main frame is another frame containing the room design
    # the room design contains the images of the furniture
    #
    def show_next_page(self): #override parent class behaviour
        self.controller.destroy()

    def __init__(self, parent, controller):

        super().__init__(
            parent, controller
        )  # call the constructor for the parent class (gui_frame)


        self.furniture_widgets = []
        self.current_design_text = tk.StringVar()

        # lbl_title = tk.Label(self, textvariable=self.title_text, anchor=tk.CENTER)
        # lbl_title.grid(column=0, row=0, columnspan=3, sticky=(tk.N, tk.S, tk.E, tk.W))

        fra_unused = tk.Frame(self.mainframe)
        fra_unused.pack(padx = 5, pady = 5, side=tk.RIGHT, fill = tk.Y, expand=tk.YES)

        lbl_unused = tk.Label(fra_unused, text="Unused items", anchor=tk.CENTER)
        lbl_unused.pack(padx=5, pady=5, fill=tk.BOTH, expand=tk.YES)

        fra_furniture_list = tk.Frame(fra_unused)  # holds listbox and scrollbar
        fra_furniture_list.pack(padx=5, pady=5, side=tk.TOP, fill=tk.Y, expand=tk.YES)

        scroll_furniture = tk.Scrollbar(fra_furniture_list, orient=tk.VERTICAL)
        self.lbx_unused = tk.Listbox(fra_furniture_list, yscrollcommand=scroll_furniture.set)

        scroll_furniture.config(command=self.lbx_unused.yview)
        scroll_furniture.pack(side=tk.RIGHT, fill=tk.Y)
        self.lbx_unused.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)



        fra_design = tk.Frame(self.mainframe)
        fra_design.pack(padx = 5, pady = 5, side=tk.LEFT, fill = tk.BOTH, expand=tk.YES)

        lbl_design_number = tk.Label(fra_design, textvariable=self.current_design_text, anchor=tk.CENTER)
        lbl_design_number.pack(padx=5, pady=5, side=tk.TOP, fill = tk.X, expand=tk.YES)

        self.fra_grid = tk.Frame(fra_design) #this holds the actual room designs
        self.fra_grid.pack(padx=5, pady=5, fill = tk.BOTH, expand=tk.YES)

        fra_navigation = tk.Frame(fra_design)
        fra_navigation.pack(padx = 5, pady = 5, side=tk.BOTTOM, fill = tk.X, expand=tk.YES)

        btn_previous_design = tk.Button(fra_navigation, text="<", command=lambda: self.load_previous_design())
        btn_previous_design.pack(padx=5, pady=5, side=tk.LEFT, fill = tk.X, expand=tk.YES)

        btn_next_design = tk.Button(fra_navigation, text=">", command=lambda: self.load_next_design())
        btn_next_design.pack(padx=5, pady=5, side=tk.RIGHT, fill = tk.X, expand=tk.YES)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(2, weight=10)
        # self.columnconfigure(3, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=3)
        # self.rowconfigure(3, weight=0)

        self.btn_next.configure(text ="Done")


    def on_show_frame(self, event, arg):
        # fires when page is loaded
        self.set_title("Room layouts for: " + str(self.controller.get_room_name()))
        self.current_design = -1
        self.load_next_design()

    def load_previous_design(self):
        # update reference to room design to load
        self.current_design = abs(
            (self.current_design - 1) % len(self.controller.room_designs)
        )
        current_room = self.controller.room_designs[self.current_design]

        self.load_design(current_room)

    def load_next_design(self):

        # update reference to room design to load
        self.current_design = (self.current_design + 1) % len(
            self.controller.room_designs
        )
        current_room = self.controller.room_designs[self.current_design]

        self.load_design(current_room)

    def load_design(self, current_room):

        # print ( 'loading design number ', self.current_design ) #debug
        self.current_design_text.set("Design number: " + str(self.current_design))

        self.lbx_unused.delete(0, tk.END)  # clear the unused entries
        # load the new set of unused entries
        # clear the room grid

        if self.my_grid is not None:
            self.my_grid.destroy()

        # reset the room frame
        self.my_grid = gi.Cell_Grid(self.fra_grid, current_room, 30)
        self.my_grid.pack(fill = tk.BOTH, expand= tk.TRUE)
        self.fra_grid.configure(background="grey")

        # populate the room grid

        for this_item in current_room.get_furniturelist():

            if this_item.is_placed():

                pass

            else:
                self.lbx_unused.insert(
                    tk.END, this_item.get_name()
                )  # add to unusued list

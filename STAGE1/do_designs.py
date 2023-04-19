import tkinter as tk
import gui_frame as gu
import room_items as ri
import gui_grid as gi 
import room_algos as al

# shows the room and selected furniture
# generates the designs

class do_designs(gu.gui_frame):

    my_grid = None
    furniture_list = None # the list of furniture selected by user for this room
    status_text = None # status of design generation

    # show the radio buttons and reset button
    # show a grid the size of the room
    #  populate the grid with the contents of the room

    def __init__(self, parent, controller):

        super().__init__(
            parent, controller
        )  # call the constructor for the parent class (gui_frame)
        
        self.furniture_list = tk.StringVar() # the list of furniture selected by user for this room
        self.status_text = tk.StringVar() # status of design generation

        self.load_room_into_grid() #pack(side = tk.LEFT, fill = tk.BOTH, expand= tk.TRUE)

        fra_rhs = tk.Frame(self.mainframe)  
        fra_rhs.pack(side=tk.RIGHT, fill = tk.BOTH, anchor= tk.N)

        tk.Label(fra_rhs, text="Furniture to be used", anchor=tk.CENTER).pack(
            side=tk.TOP, fill=tk.X, padx=5, pady=2)

        tk.Message(fra_rhs, textvariable = self.furniture_list).pack(
            side = tk.TOP, fill= tk.X, padx = 5, pady=2, anchor = tk.N, expand = tk.TRUE)
        
        tk.Button(fra_rhs, text = 'Generate designs', command=lambda: self.generate_designs()).pack(side = tk.TOP, fill = tk.X, padx=5, pady=2)


        tk.Message(self.mainframe, textvariable = self.status_text).pack(
                    side = tk.RIGHT, fill = tk.BOTH, padx=5, pady=2, expand = tk.TRUE, anchor = tk.N
        )

    def load_room_into_grid(self):
        # first, destroy the current grid (if it exists)
        if self.my_grid is not None:
            self.my_grid.destroy()

        self.my_grid = gi.Cell_Grid(self.mainframe, 
                    self.controller.base_room,
                    15, None, None)

        self.my_grid.pack(side = tk.LEFT, fill = tk.BOTH, expand= tk.TRUE)


    def on_show_frame(self, event, arg):
        # fires when page is loaded
        self.set_title(
            "Generate room designs for: " + str(self.controller.get_room_name())
        )
        self.load_room_into_grid()
        self.refresh_furniture_list()
        self.refresh_status()

    def refresh_status(self):
        self.status_text.set('Algorithms to be applied:')
        
        for i in self.controller.base_room.get_design_algos():
             
             self.add_status_text( i(self.controller.base_room).get_name() )

    def refresh_furniture_list(self):
        # load the furniture list with the furniture to be added into the room
        self.furniture_list.set('')
        for i in self.controller.base_room.furniturelist:
            self.furniture_list.set( self.furniture_list.get() + '\n' + i.name )

    def add_status_text(self, str_to_add):

        self.status_text.set( self.status_text.get() + '\n' + str_to_add)

    def generate_designs(self):

        algos = []
        for i in self.controller.base_room.get_design_algos():
            algos.append( i(self.controller.base_room) ) 

        self.controller.designs=[] # reset the generated designs

        # for each algo, make a copy of the room
        # give the design_generator the room and the algo
        # get back an updated room
        
        generator = al.design_generator( self.controller.base_room )

        for this_algo in algos:

            self.add_status_text('Applying: ' + this_algo.get_name())
            self.update_idletasks() #update screen

            self.controller.room_designs.append( generator.apply_algo( this_algo ))


        pass



        # # add a table
        # controller.base_room.add_to_furniturelist( ri.Table('Table'))
        # # add a chair
        # controller.base_room.add_to_furniturelist( ri.Table('Chair'))
        # self.refresh_furniture_list()

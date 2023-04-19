import tkinter as tk
import gui_frame as gu
import room_furniture as rf
import room_items as ri 
import python_array_test as rm

class room_dimensions(gu.gui_frame):

    widthentry = None  # entry box for width
    lengthentry = None  # entry box for length

    def add_doors_and_walls(self):

        try:
            roomwidthval = int(self.widthentry.get())
            roomlengthval = int(self.lengthentry.get())

            if roomwidthval <= 0 or roomlengthval <= 0 or roomwidthval > 25 or roomlengthval > 25:
                pass
                self.beep_bad()
            else:

                # if the room size has changed from what it was, then initialise the room
                # otherwise, don't - because this might just be clicking back/next 
                if self.controller.base_room.get_room_dims()[0] != roomwidthval or self.controller.base_room.get_room_dims()[1] != roomlengthval:
    
                    self.setup_room_obj_and_walls(self.controller, roomwidthval,roomlengthval) # initialise the room

                
                super().show_next_page()

        except ValueError:
            pass  # number not entered, show error

    #make this static so it can be called from test functions without having to enter data in all the fields on this page
    @staticmethod 
    def setup_room_obj_and_walls(controller, roomwidthval, roomlengthval):
        controller.set_room_dims(roomlengthval, roomwidthval) # initialise the room
        #set the x walls
        for y in (0, len(controller.base_room.Base)-1):
            for x in range(0, len(controller.base_room.Base[0])):
                controller.base_room.Base[y][x] = ri.Wall
        
        #set the y walls
        for y in range(0, len(controller.base_room.Base)):
            for x in (0, len(controller.base_room.Base[0])-1):
                controller.base_room.Base[y][x] = ri.Wall

    def show_next_page(self): #override parent class behaviour
            
            self.add_doors_and_walls() # do the page validation when next is clicked


    def __init__(self, parent, controller):

        super().__init__(
            parent, controller
        )  # call the constructor for the parent class (gui_frame)

        self.selectedroomwidth = tk.StringVar()
        self.selectedroomlength = tk.StringVar()

        max_column = 3
        max_row = 3


        widthtxt = tk.Label(self.mainframe, text="metres", anchor=tk.CENTER)
        lengthtxt = tk.Label(self.mainframe, text="metres", anchor=tk.CENTER)

        self.widthentry = tk.Entry(self.mainframe, textvariable=self.selectedroomwidth)
        self.widthentry.focus()
        self.widthentry.bind(
            "<Return>", lambda event: self.add_doors_and_walls()
        )  # try navigate next frame on enter key

        self.lengthentry = tk.Entry(self.mainframe, textvariable=self.selectedroomlength)
        self.lengthentry.bind(
            "<Return>", lambda event: self.add_doors_and_walls()
        )  # try navigate next frame on enter key


        widthtxt.grid(column=2, row=1, sticky=("nsew"))
        lengthtxt.grid(column=2, row=2, sticky=("nsew"))

        self.widthentry.grid(column=1, row=1, sticky=("ew"))
        self.lengthentry.grid(column=1, row=2, sticky=("ew"))

        tk.Label(self.mainframe, text="Width (x):", anchor=tk.CENTER).grid(
            column=0, row=1, sticky=("ew")
        )
        tk.Label(self.mainframe, text="Length (y):", anchor=tk.CENTER).grid(
            column=0, row=2, sticky=("ew")
        )

        for i in range(0, max_column):
            self.mainframe.columnconfigure(i, weight=2)

        for i in range(0, max_row):
            self.mainframe.rowconfigure(i, weight=2)

    def on_show_frame(self, event, arg):
        # fires when page is loaded
        self.set_title(
            "Room dimensions for: " + str(self.controller.get_room_name())
        )


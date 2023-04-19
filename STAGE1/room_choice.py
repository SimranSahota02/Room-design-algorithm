import tkinter as tk
import gui_frame as gu
import room_dimensions as rd
import python_array_test as rm

class room_choice(gu.gui_frame):

    selected_room_id = None
    # nextbtn = None  # next button

    def room_chosen(self, roomtype_class):
        self.selected_room_id = roomtype_class
        self.btn_next["state"] = tk.NORMAL
        self.controller.set_room_name(self.selected_room_id.__name__.replace('_',' '))
        self.controller.base_room = self.selected_room_id()
        self.update_title()

    def show_next_page(self): #override parent class behaviour
        if self.selected_room_id is not None:
            
            # if the base room is not of the same type as the selected room, then replace it
            if not isinstance(self.controller.base_room, self.selected_room_id):
                self.controller.base_room = self.selected_room_id()

            super().show_next_page()

    def __init__(self, parent, controller):

        super().__init__(
            parent, controller
        )  # call the constructor for the parent class (gui_frame)

        self.set_title("Select your room")

        roomchoosebtn_B = tk.Button(
            self.mainframe,
            text="Bedroom",
            name="bedroom",
            command=lambda: self.room_chosen(rm.Bedroom),width = 10, height = 5
        )
        roomchoosebtn_D = tk.Button(
            self.mainframe,
            text="Dining room",
            name="dining room",
            command=lambda: self.room_chosen(rm.Dining_Room),width = 10
        )
        roomchoosebtn_K = tk.Button(
            self.mainframe,
            text="Kitchen",
            name="kitchen",
            command=lambda: self.room_chosen(rm.Kitchen),width = 10
        )
        roomchoosebtn_L = tk.Button(
            self.mainframe,
            text="Living room",
            name="living room",
            command=lambda: self.room_chosen(rm.Living_Room),width = 10
        )
        roomchoosebtn_S = tk.Button(
            self.mainframe,
            text="Study",
            name="study",
            command=lambda: self.room_chosen(rm.Study),width = 10
        )



        roomchoosebtn_B.pack(side=tk.LEFT, fill=tk.BOTH, padx=2, pady=0, expand=tk.TRUE)
        roomchoosebtn_D.pack(side=tk.LEFT, fill=tk.BOTH, padx=2, pady=0, expand=tk.TRUE)
        roomchoosebtn_K.pack(side=tk.LEFT, fill=tk.BOTH, padx=2, pady=0, expand=tk.TRUE)
        roomchoosebtn_L.pack(side=tk.LEFT, fill=tk.BOTH, padx=2, pady=0, expand=tk.TRUE)
        roomchoosebtn_S.pack(side=tk.LEFT, fill=tk.BOTH, padx=2, pady=0, expand=tk.TRUE)

        self.btn_next.configure(state=tk.DISABLED)
        
    def on_show_frame(self, event, arg):
        # fires when page is loaded
        self.update_title()
    
    def update_title(self):
        self.set_title(
            "Selected room: " + str(self.controller.get_room_name())
        )
import tkinter as tk
import gui_frame
import show_room as sr
import room_items as ri


class room_furniture(gui_frame.gui_frame):

    lbx_furniture = None
    btn_add = None #adds an item to the list of furniture that should go in the room

    furniture_to_go_in_room = None  # list to hold the frame for each row
    fra_furniture_list = None  # frame for added furniture items

    fra_add_furniture = None  # frame for list of available furniture items
    available_furniture = None  # list of available furniture classes


    def __init__(self, parent, controller):

        super().__init__(
            parent, controller
        )  # call the constructor for the parent class (gui_frame)

        tk.Label(self.mainframe, text="", anchor=tk.CENTER).grid(
            column=0, row=1, columnspan=2, sticky="nsew", padx=5, pady=5
        )
        tk.Label(self.mainframe, text="", anchor=tk.CENTER).grid(
            column=2, row=1, columnspan=2, sticky="nsew", padx=5, pady=5
        )

        # scroll a frame needs a frame, inside which is a canvas + scrollbar, inside that goes the frame for the added furniture
        self.can_list_holder = tk.Canvas(self.mainframe, borderwidth=0)
        self.fra_furniture_list = tk.Frame(
            self.can_list_holder
        )  # the furniture added to the room
        self.scroll_furniture_list = tk.Scrollbar(
            self.mainframe, orient="vertical", command=self.can_list_holder.yview
        )
        self.can_list_holder.configure(yscrollcommand=self.scroll_furniture_list.set)

        self.scroll_furniture_list.grid(column=1, row=2, sticky="nsw")
        self.can_list_holder.grid(column=0, row=2, sticky="nsew")
        self.can_list_holder.create_window(
            (0, 0),
            window=self.fra_furniture_list,
            anchor="nw",
            tag="fra_furniture_list",
        )

        self.fra_furniture_list.bind("<Configure>", self.onFrameConfigure)
        self.can_list_holder.bind("<Configure>", self.resize_frame)

        self.fra_add_furniture = tk.Frame(self.mainframe)
        self.fra_add_furniture.grid(
            column=2, row=2, columnspan=2, sticky="nsew", padx=5, pady=5
        )

        lbl_image = tk.Label(
            self.fra_add_furniture, anchor=tk.CENTER, background="white"
        )
        lbl_image.grid(column=0, row=0, columnspan=1, sticky="nsew", padx=0, pady=10)

        fra_furniture_lbx = tk.Frame(
            self.fra_add_furniture
        )  # holds listbox and scrollbar
        fra_furniture_lbx.grid(column=0, row=1, sticky="nsew")

        # listbox for the items the user can add
        scroll_furniture_lbx = tk.Scrollbar(fra_furniture_lbx, orient=tk.VERTICAL)
        self.lbx_furniture = tk.Listbox(
            fra_furniture_lbx, yscrollcommand=scroll_furniture_lbx.set
        )
        self.lbx_furniture.bind(
            "<Double-Button>", lambda x: self.add_row()
        )  # double click is add item

        scroll_furniture_lbx.config(command=self.lbx_furniture.yview)
        scroll_furniture_lbx.pack(side=tk.RIGHT, fill=tk.Y)
        self.lbx_furniture.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.btn_add = tk.Button(
            self.fra_add_furniture, text="Add", command=lambda: self.add_row()
        )

        self.btn_add.grid(column=1, row=1, sticky="new", padx=5, pady=5)  # for testing

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=5)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)

        self.initialise_data()  # load up the raw data

        for i in self.available_furniture:
            self.lbx_furniture.insert(tk.END, i[0])

    def resize_frame(self, event):
        # make the frame in the canvas fit the canvas fully
        self.can_list_holder.itemconfig(
            "fra_furniture_list",
            height=self.can_list_holder.winfo_height(),
            width=self.can_list_holder.winfo_width(),
        )

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.can_list_holder.configure(scrollregion=self.can_list_holder.bbox("all"))

    def on_show_frame(self, event, arg):
        # fires when page is loaded
        self.set_title(
            "Choose and prioritise furniture for: "
            + str(self.controller.get_room_name())
        )

    def show_next_page(self): #override parent class behaviour
            
            self.controller.base_room.set_furniturelist(self.furniture_to_go_in_room) # load the furniture list into the controller
            super().show_next_page() # show the next page

    # add a selected-items row
    def add_row(self):
        if len(self.lbx_furniture.curselection()) > 0:

            available_furniture_item_class = self.available_furniture[
                self.lbx_furniture.curselection()[0]
            ][1]
            available_furniture_item_name = self.available_furniture[
                self.lbx_furniture.curselection()[0]
            ][0]

            self.add_furniture_at_row(
                len(self.furniture_to_go_in_room),
                available_furniture_item_class(
                    available_furniture_item_name
                ),  # pass in the name to constructor
            )

    # add  selected furniture
    def add_furniture_at_row(self, location, furniture_to_add):
        self.furniture_to_go_in_room.append(
            furniture_to_add
        )  # update the list of furniture
        self.add_furniture_at_row_gui(location, furniture_to_add)  # update the screen

    # add a selected-items row at a specific position in list
    # create a row in the selected-items list
    # populate the new row with info from the item selected in the listbox
    # use a grid so that it is easy to move them up and down
    def add_furniture_at_row_gui(self, location, furniture_to_add):

        fra_this_row = tk.Frame(self.fra_furniture_list)

        # grid rows = number of items in the furniture list
        fra_this_row.grid(row=location, column=0, sticky="nsew")

        tk.Label(
            fra_this_row,
            text=furniture_to_add.get_name(),  # + str(len(self.furniture_to_go_in_room)),
            anchor=tk.W,
            width=10,
        ).pack(side=tk.LEFT, fill=tk.X, padx=2, pady=2, expand=tk.TRUE)
        tk.Label(fra_this_row, text="Width:", anchor=tk.CENTER).pack(
            side=tk.LEFT, fill=tk.X, padx=2, pady=2, expand=tk.TRUE
        )

        ent = tk.Entry(fra_this_row, width=6)
        ent.insert(0, furniture_to_add.get_dimx())
        ent.pack(side=tk.LEFT, fill=tk.X, padx=2, pady=2, expand=tk.TRUE)
        ent.bind("<Leave>", lambda event, entr=(location, ent): self.dimx_changed(entr))
        ent.bind(
            "<KeyRelease>", lambda event, entr=(location, ent): self.dimx_changed(entr)
        )

        tk.Label(fra_this_row, text="Length:", anchor=tk.CENTER).pack(
            side=tk.LEFT, fill=tk.X, padx=2, pady=2, expand=tk.TRUE
        )
        ent = tk.Entry(fra_this_row, width=6)
        ent.insert(0, furniture_to_add.get_dimy())
        ent.pack(side=tk.LEFT, fill=tk.X, padx=2, pady=2, expand=tk.TRUE)
        ent.bind(
            "<Leave>", lambda event, entr=(location, ent): self.dimy_changed(entr)
        )  # for mouse events
        ent.bind(
            "<KeyRelease>", lambda event, entr=(location, ent): self.dimy_changed(entr)
        )  # for key events

        tk.Button(
            fra_this_row, text="▲", command=lambda: self.move_row(location, -1)
        ).pack(side=tk.LEFT, fill=tk.X, padx=1, pady=2, expand=tk.TRUE)
        tk.Button(
            fra_this_row, text="▼", command=lambda: self.move_row(location, 1)
        ).pack(side=tk.LEFT, fill=tk.X, padx=1, pady=2, expand=tk.TRUE)
        tk.Button(
            fra_this_row, text="-", command=lambda: self.delete_row(location)
        ).pack(side=tk.LEFT, fill=tk.X, padx=1, pady=2, expand=tk.TRUE)

    def dimy_changed(self, entry):
        self.furniture_to_go_in_room[entry[0]].set_dimy(entry[1].get())

    def dimx_changed(self, entry):
        self.furniture_to_go_in_room[entry[0]].set_dimx(entry[1].get())

    # delete a selected items row
    def delete_row(self, row_to_delete):
        print(row_to_delete)
        del self.furniture_to_go_in_room[row_to_delete]
        self.refresh_furniture_to_go_in_room_gui()
        pass

    # move a selected items location
    # -1, +1 for up/down
    def move_row(self, location, change):
        if (location + change) >= 0 and (location + change) < len(
            self.furniture_to_go_in_room
        ):
            (
                self.furniture_to_go_in_room[location],
                self.furniture_to_go_in_room[location + change],
            ) = (
                self.furniture_to_go_in_room[location + change],
                self.furniture_to_go_in_room[location],
            )
            self.refresh_furniture_to_go_in_room_gui()

    # populate the frame with all the furniture the user has chosen
    def refresh_furniture_to_go_in_room_gui(self):

        if self.fra_furniture_list is not None:
            for (
                widget
            ) in (
                self.fra_furniture_list.winfo_children()
            ):  # delete everything in the frame
                widget.destroy()

        for i in range(0, len(self.furniture_to_go_in_room)):
            self.add_furniture_at_row_gui(i, self.furniture_to_go_in_room[i])
        pass

    def initialise_data(self):
        self.furniture_to_go_in_room = (
            []
        )  # initialise the list of furniture the user has selected

        # load the listbox with furniture
        self.available_furniture = ri.Furniture.get_available_furniture_types()

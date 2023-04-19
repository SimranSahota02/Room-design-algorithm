import tkinter as tk
import winsound

# this frame has a help, next and back button
# other frames inherit from it

class gui_frame(tk.Frame):  # new class all the screens inherit from, holds 'controller'

    controller = None # passes data between pages

    def __init__(self, parent, controller):

        self.controller = controller
        self.title_text = tk.StringVar()  # use this to hold the frame title
        tk.Frame.__init__(self, parent) 

        self.title = tk.Label(self, textvariable = self.title_text, name="title", anchor=tk.CENTER)
        self.title.pack(side=tk.TOP,fill = tk.X, expand = tk.TRUE )
        self.mainframe = tk.Frame(self, relief=tk.RAISED, borderwidth=1) # mainframe holds the 'guts' of the page


        self.mainframe.pack(side=tk.TOP, fill = tk.BOTH, expand = tk.TRUE)
        fra_nav = tk.Frame(self)

        fra_nav.pack(side=tk.BOTTOM, fill = tk.X,expand = tk.TRUE)

        self.btn_next = tk.Button(fra_nav, text="Next", name = "next", command=lambda:self.show_next_page())
        self.btn_back = tk.Button(fra_nav, text="Back", name = "back", command=lambda:self.show_previous_page())
        self.btn_help = tk.Button(fra_nav, text="Help", name = "help", command=lambda:self.show_help())


        self.btn_next.pack(side=tk.RIGHT, fill=tk.X, padx=2, pady=2, expand=tk.FALSE)
        self.btn_help.pack(side=tk.RIGHT, fill=tk.X, padx=2, pady=2, expand=tk.FALSE)
        self.btn_back.pack(side=tk.LEFT, fill=tk.X, padx=2, pady=2, expand=tk.FALSE)

        self.bind(
            "<<ShowFrame>>",
            lambda event, arg=controller.get_room_name(): self.on_show_frame(
                event, arg
            ),
        )

    def set_title(self, title_text):
        self.title_text.set(title_text)

    def show_next_page(self):
        self.controller.show_next_page()    

    def show_previous_page(self):
        self.controller.show_previous_page()

    def show_help(self):
        self.controller.help_popup()

    def on_show_frame(self, event, arg):
            # fires when page is loaded
            self.set_title(
                "Default room: " + str(self.controller.get_room_name())
            )

    
    @staticmethod
    def beep_good():
        
        winsound.Beep(2500, 50) #ding)

        
    @staticmethod
    def beep_bad():
        
        winsound.Beep(500, 50) #ding)
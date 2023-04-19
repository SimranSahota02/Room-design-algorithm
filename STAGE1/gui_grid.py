import tkinter as tk
import room_items as ri
import gui_frame as gi

class Cell():
    EMPTY_COLOUR_BORDER = "#c1c1c1"

    #dict, colours shown for each room item  type
    colours_for_items = {
            ri.Wall : 'grey',
            ri.Door : 'yellow',
            ri.Lamp : 'grey',
            ri.Table : 'grey',
            ri.Coffee_table : 'grey',
            ri.Breakfast_bar : 'grey',
            ri.Chair : 'grey',
            ri.Armchair : 'grey',
            ri.Stool : 'grey',
            ri.Sofa : 'grey',
            ri.Cabinet : 'grey',
            ri.Bed : 'grey',
            ri.Sink : 'grey',
            ri.Oven : 'grey',
            ri.Fridge : 'grey',
            ri.Dishwasher : 'grey',
            ri.Bin : 'grey',
            ri.Dryer : 'grey',
            ri.Kitchen_counter : 'grey',
            ri.Microwave : 'grey',
            ri.Bean_bag : 'grey',
            ri.Vase : 'grey',
            ri.TV : 'grey',
            None: 'white' #empty
        }

    def __init__(self, master, x, y, sizex, sizey, item_type):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.sizex= sizex
        self.sizey= sizey
        self.item_type = item_type

    def _switch(self):
        """ Switch if the cell is filled or not. """
        self.fill= not self.fill

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = self.colours_for_items[self.item_type]
            
            outline = Cell.EMPTY_COLOUR_BORDER

            xmin = self.abs * self.sizex 
            xmax = xmin + self.sizex 
            ymin = self.ord * self.sizey 
            ymax = ymin + self.sizey 

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)

    # returns the room item class representing what is in the cell
    def room_item_shown(self):
        return self.item_type

class Cell_Grid(tk.Canvas):

    wscale = None
    hscale = None
    cellSizeX = None
    cellSizeY = None

    def __init__(self,master, room_contents, cell_Size, radiobutton_var = None, addable_items = None, *args, **kwargs):

        self.radiobutton_var = radiobutton_var
        self.addable_items = addable_items
        self.room_contents = room_contents

        rows = room_contents.get_room_dims_cells()[1]
        cols = room_contents.get_room_dims_cells()[0]
        self.cellSizeX = cell_Size
        self.cellSizeY = cell_Size

        tk.Canvas.__init__(self, master, width = self.cellSizeX * cols ,
                         height = self.cellSizeY * rows, *args, **kwargs)
        
        self.configure(highlightthickness=0)
        self.bind("<Configure>", self.on_resize) #resizing code
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self.grid_squares = []

        for row in range(rows):

            line = []
            for column in range(cols):
                 line.append(Cell(self, column, row, self.cellSizeX, self.cellSizeY, room_contents.Base[row][column]))

            self.grid_squares.append(line)

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #bind click action
        self.bind("<Button-1>", self.handleMouseClick)  

        self.draw()

        for item in room_contents.furniturelist:
            if item.is_placed() is True:
                xmin = item.get_location()[0] 
                ymin = item.get_location()[1] 
                xmax = item.get_dimx() + item.get_location()[0]
                ymax = item.get_dimy() + item.get_location()[1] 

                self.create_rectangle(xmin*self.cellSizeX,ymin*self.cellSizeY, xmax*self.cellSizeX, ymax*self.cellSizeY, outline = "white", fill = "green")
                self.create_text(self.cellSizeX * (xmin + item.get_dimx()/2),self.cellSizeY * (ymin + item.get_dimy()/2), fill ="white", font=("helvetica", "9"),text=item.name)
            
    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        self.wscale = float(event.width)/self.width
        self.hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,self.wscale,self.hscale)
        self.cellSizeX = self.cellSizeX * self.wscale
        self.cellSizeY = self.cellSizeY * self.hscale

    def draw(self):
        for row in self.grid_squares:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSizeY)
        column = int(event.x / self.cellSizeX)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        self.handleMouseClickRC(row, column)

    #use this call directly only for testing instead of simulating a mouse click event
    def handleMouseClickRC(self, row, column):

        # trying to add
        item_to_add = self.addable_items[ int( self.radiobutton_var.get()) ]

        cell = self.grid_squares[row][column]
        
        #print(item_to_add in ri.room_item.can_replace_with(cell.room_item_shown()), 'adding ', item_to_add, ' over a ', cell.room_item_shown())
        if item_to_add in ri.room_item.can_replace_with(cell.room_item_shown()):

            cell.item_type  = item_to_add
            self.room_contents.Base[row][column] = item_to_add
            
            cell.sizex = self.cellSizeX
            cell.sizey = self.cellSizeY

            cell.draw()
            gi.gui_frame.beep_good() #ding
        else:
            gi.gui_frame.beep_bad() #ding


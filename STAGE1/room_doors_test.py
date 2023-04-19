import unittest 
import room_dimensions
import launch_gui
import room_doors as rd
import room_items as ri
import python_array_test as ro
import gui_grid as gi

class Test_room_doors(unittest.TestCase):
    def setUp(self):
        self.app = launch_gui.main_gui()
        self.load_page(rd.room_doors)
        self.app.update() # loads the screen

    def load_page(self, page_class):
        
        for i in self.app.pages_list:
            if isinstance(i, page_class):
                self.app.show_page(i) #load the page

    def setup_a_room(self, x, y):
        room_dimensions.room_dimensions.setup_room_obj_and_walls(self.app, x, y)
        self.app.active_page.load_room_into_grid()
        self.app.update() # loads the screen

    def tearDown(self):
        self.app.destroy()

    def get_the_grid(self):
                # expect grid frame visible
        for widget in self.app.active_page.children['!frame'].winfo_children():
            if isinstance(widget, gi.Cell_Grid):
                the_grid = widget
                break
        return the_grid

    def test_show_page(self):
        for i in self.app.pages_list:
            if isinstance( i, rd.room_doors):
                self.app.show_page( i )

        self.assertIsInstance(self.app.active_page, rd.room_doors)

    def test_show_room_grid(self):
        
        # setup the room obj 
        x=1
        y=2
        self.setup_a_room(x,y)

        the_grid = self.get_the_grid()
        self.assertIsNotNone(the_grid)

        # expect grid size matches room that's been setup
        self.assertTrue( len(the_grid.grid_squares) == ro.room.dims2cells(y))
        self.assertTrue( len(the_grid.grid_squares[0]) == ro.room.dims2cells(x))

        # expect all perimiter cells to be represented as wall cells in the grid
        for row in (0, ro.room.dims2cells(y)-1): # both length walls
            for col in range(0, ro.room.dims2cells(x)-1): 
                self.assertTrue(the_grid.grid_squares[row][col].room_item_shown() == ri.Wall )

        for row in range(0, ro.room.dims2cells(y)-1): 
            for col in (0, ro.room.dims2cells(x)-1): # both width walls
                self.assertTrue(the_grid.grid_squares[row][col].room_item_shown() == ri.Wall )

        

    # def test_reset_layout(self):
    #     self.assertTrue(False)

    
    def test_add_doors(self):
        
        # setup the room obj 
        x=1
        y=2
        self.setup_a_room(x,y)
        the_grid = self.get_the_grid()
        widthx_cells = ro.room.dims2cells(x)
        lengthy_cells = ro.room.dims2cells(y)

        # with  select door rbtn  selected
        self.app.active_page.rb_door.invoke()
        
        
        # click on space does nothing

        self.assertIsNone(the_grid.grid_squares[2][2].room_item_shown()) #screen cell empty
        self.assertIsNone(self.app.base_room.Base[2][2] ) #empty already there
        the_grid.handleMouseClickRC(2, 2) # tryp to put a door in 
        self.app.update() #update screen
        self.assertIsNone(the_grid.grid_squares[2][2].room_item_shown()) #screen cell unchanged
        self.assertIsNone(self.app.base_room.Base[2][2] ) #empty still 

        # click on wall changes cell to door
        # and puts a door in the room
        self.assertTrue(the_grid.grid_squares[lengthy_cells-1][widthx_cells-1].room_item_shown() == ri.Wall) #screen cell shows wall
        self.assertTrue(self.app.base_room.Base[lengthy_cells-1][widthx_cells-1] == ri.Wall) #wall already there
        the_grid.handleMouseClickRC(lengthy_cells-1, widthx_cells-1) #put a door in bottom right corner
        self.app.update() #update screen
        self.assertTrue(the_grid.grid_squares[lengthy_cells-1][widthx_cells-1].room_item_shown() == ri.Door) #screen cell updated
        self.assertTrue(self.app.base_room.Base[lengthy_cells-1][widthx_cells-1] == ri.Door) #base updated

        # ...and then click on door does nothing
        the_grid.handleMouseClickRC(lengthy_cells-1, widthx_cells-1)
        self.assertTrue(the_grid.grid_squares[lengthy_cells-1][widthx_cells-1].room_item_shown() == ri.Door) #still a door
        self.assertTrue(self.app.base_room.Base[lengthy_cells-1][widthx_cells-1] == ri.Door) #still a door

    
    def test_add_walls(self):
        # setup the room obj 
        x=1
        y=2
        self.setup_a_room(x,y)
        the_grid = self.get_the_grid()
        # widthx_cells = ro.room.dims2cells(x)
        # lengthy_cells = ro.room.dims2cells(y)

        # with  select wall rbtn  selected
        
        self.app.active_page.rb_wall.invoke()
        # click on nothing changes to wall
        # 

        self.assertIsNone(the_grid.grid_squares[2][2].room_item_shown()) #screen cell empty
        self.assertIsNone(self.app.base_room.Base[2][2] ) #empty already there
        the_grid.handleMouseClickRC(2, 2) # tryp to put a wall in 
        self.assertTrue(the_grid.grid_squares[2][2].room_item_shown() == ri.Wall) #screen cell unchanged
        self.assertTrue(self.app.base_room.Base[2][2] == ri.Wall) #wall in the base


        # click on wall changes nothing
        self.assertTrue(the_grid.grid_squares[0][0].room_item_shown() == ri.Wall) #screen cell shows wall
        self.assertTrue(self.app.base_room.Base[0][0] == ri.Wall) #wall already there
        the_grid.handleMouseClickRC(0, 0) #put a door in bottom right corner
        self.assertTrue(the_grid.grid_squares[0][0].room_item_shown() == ri.Wall) #screen still a wall updated
        self.assertTrue(self.app.base_room.Base[0][0] == ri.Wall) #base still a wall

        # click on door changes to wall
        self.app.active_page.rb_door.invoke()
        the_grid.handleMouseClickRC(0,0) # change 0,0 to a door
        self.assertTrue(the_grid.grid_squares[0][0].room_item_shown() == ri.Door) 
        self.assertTrue(self.app.base_room.Base[0][0] == ri.Door) 

        self.app.active_page.rb_wall.invoke()
        the_grid.handleMouseClickRC(0,0) # try change 0,0 to a wall
        self.assertTrue(the_grid.grid_squares[0][0].room_item_shown() == ri.Wall) #Now a wall
        self.assertTrue(self.app.base_room.Base[0][0] == ri.Wall) # Now a wall
    
    # def test_delete_door(self):
    #     self.assertTrue(False)

    # def test_delete_wall(self):
    #     self.assertTrue(False)

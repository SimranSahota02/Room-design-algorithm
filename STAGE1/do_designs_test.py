import unittest 
import room_dimensions
import launch_gui
import room_doors as rd
import room_items as ri
import do_designs as do
import python_array_test as ro
import gui_grid as gi

class Test_do_designs_doors(unittest.TestCase):
    def setUp(self):
        self.app = launch_gui.main_gui()
        self.load_page(do.do_designs)
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
            if isinstance( i, do.do_designs):
                self.app.show_page( i )

        self.assertIsInstance(self.app.active_page, do.do_designs)

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

        pass
        
    def test_furniture_list_shown(self):
        
        # setup the room obj 
        x=1
        y=2
        self.setup_a_room(x,y)

        # add a table
        self.app.active_page.controller.base_room.add_to_furniturelist( ri.Table('Table'))
        # add a chair
        self.app.active_page.controller.base_room.add_to_furniturelist( ri.Table('Chair'))

        # load the page

        self.test_show_page()
        # expect table and chair appear in the list to be added
        self.assertTrue('Table' in self.app.active_page.furniture_list.get())
        self.assertTrue('Chair' in self.app.active_page.furniture_list.get())
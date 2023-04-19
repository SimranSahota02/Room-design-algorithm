import unittest 

import launch_gui
import room_dimensions as rd
import room_items as ri

class Test_room_dimensions(unittest.TestCase):
    def setUp(self):
        self.app = launch_gui.main_gui()
        self.load_page(rd.room_dimensions)

    def load_page(self, page_class):
        
        for i in self.app.pages_list:
            if isinstance(i, page_class):
                self.app.show_page(i) #load the page

        self.app.update() # makes the screen visible


    def tearDown(self):
        self.app.destroy()

    def test_show_page(self):
        self.assertIsInstance(self.app.active_page, rd.room_dimensions)
        
    def test_good_dimensions(self):

        x= 10
        y = 5
        self.app.active_page.widthentry.delete('0', 'end')
        self.app.active_page.widthentry.insert('0', str(x))
        self.app.active_page.lengthentry.delete('0', 'end')
        self.app.active_page.lengthentry.insert('0', str(y))

        self.assertTrue(float(self.app.active_page.selectedroomwidth.get()) == float(10)) # field value = room size entered
        self.assertTrue(float(self.app.active_page.selectedroomlength.get()) == float(5)) # field value = room size entered

        self.page_validation_and_next_page()

        self.assertTrue(len(self.app.base_room.Base) == y*2+2) # base room size = room size entered
        self.assertTrue(len(self.app.base_room.Base[0]) == x*2+2) # base room size = room size entered
        self.assertTrue(float(self.app.base_room.get_room_dims()[0]) == float(10)) # base room size = room size entered
        self.assertTrue(float(self.app.base_room.get_room_dims()[1]) == float(5)) # base room size = room size entered
        self.assertTrue(float(self.app.base_room.get_room_dims_cells()[0]) == float(x*2+2)) # base room size = room size entered
        self.assertTrue(float(self.app.base_room.get_room_dims_cells()[1]) == float(y*2+2)) # base room size = room size entered


    def page_validation_and_next_page(self):
        
        self.app.active_page.btn_next.invoke() # next page should setup the room
        self.app.update() # makes the screen visible/executes button clicks etc.

    # def test_bad_dimensions(self):
    #     x= 10.0
    #     y = 5.0
    #     self.app.active_page.widthentry.delete('0', 'end')
    #     self.app.active_page.widthentry.insert('0', str(x))
    #     self.app.active_page.lengthentry.delete('0', 'end')
    #     self.app.active_page.lengthentry.insert('0', str(y))



    #     x= 'hello'
    #     y = ''
    #     self.app.active_page.widthentry.delete('0', 'end')
    #     self.app.active_page.widthentry.insert('0', str(x))
    #     self.app.active_page.lengthentry.delete('0', 'end')
    #     self.app.active_page.lengthentry.insert('0', str(y))


    #     self.assertTrue(False)

    def test_setup_room_obj(self):

        # setup the room size, 
        x= 3
        y = 1
        self.app.active_page.widthentry.delete('0', 'end')
        self.app.active_page.widthentry.insert('0', str(x))
        self.app.active_page.lengthentry.delete('0', 'end')
        self.app.active_page.lengthentry.insert('0', str(y))


        self.page_validation_and_next_page() #trigger setup of room obj

        # expect room obj to be sized 2 * each dimension + 2 cells long (so 10m wall becomes 22 cells)
        self.assertTrue( len(self.app.base_room.Base[0]) == x*2+2 )
        self.assertTrue( len(self.app.base_room.Base) == y*2+2 )
        
        # expect inner cells to be empty
        for x in range(1, len(self.app.base_room.Base[0])-2): # both length walls
            for y in range(1, len(self.app.base_room.Base)-2): # both width walls
                self.assertIsNone( self.app.base_room.Base[y][x] )

        # expect all perimiter cells to contain a wall class
        for x in (0, len(self.app.base_room.Base[0])-1): # both length walls
            for y in range(0, len(self.app.base_room.Base)-1): 
                self.assertTrue(self.app.base_room.Base[y][x] == ri.Wall )
        for x in range(0, len(self.app.base_room.Base[0])-1): 
            for y in (0, len(self.app.base_room.Base)-1): # both width walls
                self.assertTrue(self.app.base_room.Base[y][x] == ri.Wall )



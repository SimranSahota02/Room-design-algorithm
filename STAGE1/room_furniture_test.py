import unittest 
import room_dimensions
import launch_gui
import room_doors as rd
import room_items as ri
import room_furniture as rf
import python_array_test as ro
import gui_grid as gi
import tkinter as tk

class Test_room_furniture(unittest.TestCase):
    def setUp(self):
        self.app = launch_gui.main_gui()
        self.load_page(rf.room_furniture)
        self.app.update() # loads the screen

    def load_page(self, page_class):
        
        for i in self.app.pages_list:
            if isinstance(i, page_class):
                self.app.show_page(i) #load the page

    def setup_a_room(self, x, y):
        room_dimensions.room_dimensions.setup_room_obj_and_walls(self.app, x, y)
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
            if isinstance( i, rf.room_furniture):
                self.app.show_page( i )

        self.assertIsInstance(self.app.active_page, rf.room_furniture)

    def get_index_of_furniture(self, item_name):
        try:
            index = self.app.active_page.lbx_furniture.get(0, "end").index(item_name)
        except ValueError:
            index = None
        
        return index

    BUTTON_CLICK=0
    LISTBOX_DOUBLE_CLICK = 1
    def add_a_furniture_item(self, item_name, method):
        
        index = self.get_index_of_furniture(item_name)
        self.assertIsNotNone(index) # found the item
        self.app.active_page.lbx_furniture.selection_clear(0, tk.END) #clear selection
        self.app.active_page.lbx_furniture.selection_set(index) #select the furniture selection

        if method == self.LISTBOX_DOUBLE_CLICK:
            pass # TODO create an event and fire it
        else:
            self.app.active_page.btn_add.invoke()

        
        # check it appeared at the end of the list of items to add
        self.assertIsInstance( self.app.active_page.furniture_to_go_in_room[-1],ri.Table)

        # check it appeared in the window on the left 
        #  get the last frame in the enclosing furniture frame on the left
        count_frames = 0

        for i in self.app.active_page.fra_furniture_list.children:
            if isinstance(self.app.active_page.fra_furniture_list.children[i], tk.Frame):
                count_frames = count_frames + 1

        # number of frames should match size of  furniture_to_go_in_room
        self.assertTrue ( count_frames == len (self.app.active_page.furniture_to_go_in_room) )
        
        # frame i should contain the item added - first label should say the item name
        x = self.app.active_page.fra_furniture_list.children[i]
        return x

    # def count_of_furniture_added_to_list(self, item_class):
        
    #     count =0
        
    #     for i in self.app.active_page.furniture_to_go_in_room:
    #         if isinstance(i, item_class):
    #             count = count + 1
        
    #     return count

    def test_add_table(self):
        #expect
        # find table in the list of furniture that can be added
        # adding the table 
        #  adds it to the window on the left
        #  adds it to the list of furniture to add array
        # 
       
        # setup the room obj 
        x=1
        y=2
        self.setup_a_room(x,y)
        
        item_name = 'Table'
        fra_item = self.add_a_furniture_item(item_name, self.BUTTON_CLICK)
        self.assertTrue(fra_item.children['!label'].cget('text') == item_name )        



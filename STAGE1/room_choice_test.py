import unittest
import tkinter as tk
import launch_gui
import room_choice as rc
import show_room as sr
import room_dimensions as rd
import room_furniture as rf
import room_doors as ro
import python_array_test as rm

class Test_room_choice(unittest.TestCase):
    def setUp(self):
        self.app = launch_gui.main_gui()
        #self.app.active_page = self.app.children["!frame"].children["!room_choice"]

    def tearDown(self):
        self.app.destroy()

    def select_room(self, room_button_name):

        self.assertTrue(self.app.active_page.btn_next["state"] == tk.DISABLED)
        self.app.active_page.children["!frame"].children[room_button_name].invoke()
        self.assertTrue(self.app.active_page.btn_next["state"] == tk.NORMAL)

        self.assertTrue(
            # the class names have underscores, but the button names have spaces
            self.app.active_page.selected_room_id.__name__.lower() == room_button_name.lower().replace(' ', '_')
        )

    def test_select_dining_room(self):
        self.select_room("dining room")

    def test_select_bedroom(self):
        self.select_room("bedroom")

    def test_select_living_room(self):
        self.select_room("living room")

    def test_select_study(self):
        self.select_room("study")

    def test_select_kitchen(self):
        self.select_room("kitchen")

    def test_go_next_page(self):
        # choose a room
        # click next button
        # base room type should be instance of the selected room
        # expect next page
        self.test_select_study()
        self.app.active_page.btn_next.invoke()
        self.assertIsInstance(self.app.base_room, rm.Study)
        # page is set
        self.assertIsInstance(
            self.app.active_page,
            rd.room_dimensions,
        )
        self.app.update_idletasks()
        self.app.update()
        #page is shown
        self.assertIsInstance(
            self.app.active_page,
            rd.room_dimensions,
        )

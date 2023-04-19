import unittest

import launch_gui
import room_choice


class Test_launch_gui(unittest.TestCase):
    def setUp(self):
        self.app = launch_gui.main_gui()

    def tearDown(self):
        self.app.destroy()

    # check that room choice is shown
    def test_room_choice_shown(self):
        self.assertIsInstance(
            self.app.active_page,
            room_choice.room_choice,
        )

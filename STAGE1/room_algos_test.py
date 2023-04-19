import unittest 
import room_items as ri
import python_array_test as ro
import room_algos as al


class Test_room_furniture(unittest.TestCase):
    my_room = None
    my_generator = None
    
    def setUp(self):
        pass
    
    def setup_a_room(self, x, y, room_type):
        self.my_room = room_type()
        self.my_room.set_room_size(x,y)
        
        for y in (0, len(self.my_room.Base)-1):
            for x in range(0, len(self.my_room.Base[0])):
                self.my_room.Base[y][x] = ri.Wall
        
        #set the y walls
        for y in range(0, len(self.my_room.Base)):
            for x in (0, len(self.my_room.Base[0])-1):
                self.my_room.Base[y][x] = ri.Wall
                
        self.my_generator = al.design_generator(self.my_room)
        self.my_generator.room = self.my_room

    def tearDown(self):
        #self.app.destroy()
        pass

    # 1m x 1m room with 50cm x 50cm item == 2 cell x 2 cell room with 1 cell x 1 cell item
    def test_1x1_room_1x1_item(self): 

        self.setup_a_room(1,1, ro.Kitchen)
        self.assertIsInstance(self.my_room, ro.Kitchen)

        chair = ri.Chair(name="Chair", widthx=2, lengthy=2)
        self.my_room.set_furniturelist([chair])
        my_new_room = self.my_generator.apply_algo(al.random_design(self.my_room))
        
        self.assertTrue(my_new_room.furniturelist[0].get_location()[0] == 1)
        self.assertTrue(my_new_room.furniturelist[0].get_location()[1] == 1)
        self.assertTrue(my_new_room.furniturelist[0].is_placed())
        

    def test_2x2_room_1x1_item(self):

        self.setup_a_room(1,1, ro.Kitchen)
        chair = ri.Chair()
        stool = ri.Stool()
        self.my_room.set_furniturelist([chair,stool])
        self.my_room = self.my_generator.apply_algo(al.random_design(self.my_room))
        
        print(chair.get_location())
        print(stool.get_location())
        self.assertTrue(self.my_room.furniturelist[0].is_placed())
        self.assertTrue(self.my_room.furniturelist[1].is_placed())
        self.assertIsInstance(self.my_room, ro.Kitchen)

    def test_too_big_for_room(self):

        self.setup_a_room(1,1, ro.Kitchen)
        chair = ri.Chair(name="Chair", widthx=3, lengthy=3)
        self.my_room.set_furniturelist([chair])
        self.my_generator.apply_algo(al.random_design(self.my_room))
        
        self.assertFalse(chair.is_placed())
        self.assertIsInstance(self.my_room, ro.Kitchen)

    def test_x_and_y_large_too_big_for_room(self):

        self.setup_a_room(4,2, ro.Kitchen) #4x2 meter room
        chair = ri.Chair(name="Chair", widthx=2, lengthy=4) #1x2 meter chair -- change dims
        self.my_room.set_furniturelist([chair])
        self.my_generator.apply_algo(al.random_design(self.my_room))
        
        self.assertFalse(self.my_room.furniturelist[0].is_placed())
        self.assertIsInstance(self.my_room, ro.Kitchen)

        self.setup_a_room(2,4, ro.Kitchen)
        chair = ri.Chair(name="Chair", widthx=4, lengthy=2)
        self.my_room.set_furniturelist([chair])
        self.my_generator.apply_algo(al.random_design(self.my_room))
        
        self.assertFalse(self.my_room.furniturelist[0].is_placed())
        self.assertIsInstance(self.my_room, ro.Kitchen)

    # 1m x 1m room with  4x (50cm x 50cm item) == 2 cell x 2 cell room with 1 cell x 1 cell item
    def test_1x1_room_4x_1x1_item(self): 

        self.setup_a_room(1,1, ro.Kitchen)
        self.assertIsInstance(self.my_room, ro.Kitchen)

        chairs = []
        for i in range(0,4):
            chairs.append(ri.Chair(name="Chair" + str(i), widthx=1, lengthy=1))

        self.my_room.set_furniturelist(chairs)
        my_new_room = self.my_generator.apply_algo(al.random_design(self.my_room))
        
        for i in range(0,4):
            self.assertTrue(my_new_room.furniturelist[i].is_placed())
            print(i,my_new_room.furniturelist[i].get_location())
            for j in range(0,4):
                if i == j:
                    pass
                else:
                    print(j,my_new_room.furniturelist[j].get_location())
                    self.assertFalse(my_new_room.furniturelist[i].get_location() == my_new_room.furniturelist[j].get_location())

    def test_candidates(self): 

        self.setup_a_room(1,1, ro.Kitchen)
        self.assertIsInstance(self.my_room, ro.Kitchen)

        chair = ri.Chair(name="Chair", widthx=1, lengthy=1)
        self.my_room.add_to_furniturelist(chair)
        self.my_room.place_furniture(chair,1,1)

        stool = ri.Stool(name="Stool",widthx=1, lengthy=1)
        self.my_room.add_to_furniturelist(stool)
        candidates = []
        candidates = self.my_room.collisions(1,1)

        print(candidates)
        self.assertTrue(candidates[0] == [2,1])
        self.assertTrue(candidates[1] == [1,2])
        self.assertTrue(candidates[2] == [2,2])

    def test_candidates_rectangle(self): 

        self.setup_a_room(1,2, ro.Kitchen)
        self.assertIsInstance(self.my_room, ro.Kitchen)

        chair = ri.Chair(name="Chair", widthx=1, lengthy=1)
        self.my_room.add_to_furniturelist(chair)
        self.my_room.place_furniture(chair,2,1)

        stool = ri.Stool(name="Stool",widthx=1, lengthy=1)
        self.my_room.add_to_furniturelist(stool)
        candidates = []
        candidates = self.my_room.collisions(1,1)

        print(candidates)
        self.assertTrue(candidates == [[1, 1], [1, 2], [2, 2], [1, 3], [2, 3], [1, 4], [2, 4]])

    def test_candidates_4_items(self): 

        self.setup_a_room(1,1, ro.Kitchen)
        self.assertIsInstance(self.my_room, ro.Kitchen)

        stool = ri.Stool(name="Stool",widthx=1, lengthy=1)
        self.my_room.add_to_furniturelist(stool)
        self.my_room.place_furniture(stool,2,2)
        
        candidates_1 = self.my_room.collisions(1,1)
        print(candidates_1)
        
        stool = ri.Stool(name="Stool",widthx=1, lengthy=1)
        self.my_room.add_to_furniturelist(stool)
        self.my_room.place_furniture(stool,2,1)

        candidates_2 = self.my_room.collisions(1,1)
        print(candidates_2)
        

        chair = ri.Chair(name="Chair", widthx=1, lengthy=1)
        self.my_room.add_to_furniturelist(chair)
        self.my_room.place_furniture(chair,1,1)

        candidates_3 = self.my_room.collisions(1,1)
        print(candidates_3)
        

        stool = ri.Stool(name="Stool",widthx=1, lengthy=1)
        self.my_room.add_to_furniturelist(stool)
        self.my_room.place_furniture(stool,1,2)

        candidates_4 = self.my_room.collisions(1,1)
        print(candidates_4)
        
        self.assertTrue(candidates_1 == [[1, 1],[2, 1], [1, 2]])
        self.assertTrue(candidates_2 == [[1, 1], [1, 2]])
        self.assertTrue(candidates_3 == [[1, 2]])
        self.assertTrue(candidates_4 == [])

    def test_kitchen_algo(self):

        self.setup_a_room(1,1, ro.Kitchen)
        chair = ri.Chair()
        stool = ri.Stool()
        self.my_room.set_furniturelist([chair,stool])
        self.my_room = self.my_generator.apply_algo(al.standard_kitchen(self.my_room))
        
        print(chair.get_location())
        print(stool.get_location())
        self.assertTrue(self.my_room.furniturelist[0].is_placed())
        self.assertTrue(self.my_room.furniturelist[1].is_placed())
        self.assertIsInstance(self.my_room, ro.Kitchen)

    def test_study_algo(self):

        self.setup_a_room(1,1, ro.Study)
        chair = ri.Chair()
        stool = ri.Stool()
        self.my_room.set_furniturelist([chair,stool])
        self.my_room = self.my_generator.apply_algo(al.standard_study(self.my_room))
        
        print(chair.get_location())
        print(stool.get_location())
        self.assertTrue(self.my_room.furniturelist[0].is_placed())
        self.assertTrue(self.my_room.furniturelist[1].is_placed())
        self.assertIsInstance(self.my_room, ro.Study)

    def test_bedroom_algo(self):

        self.setup_a_room(1,1, ro.Bedroom)
        chair = ri.Chair()
        stool = ri.Stool()
        self.my_room.set_furniturelist([chair,stool])
        self.my_room = self.my_generator.apply_algo(al.standard_bedroom(self.my_room))
        
        print(chair.get_location())
        print(stool.get_location())
        self.assertTrue(self.my_room.furniturelist[0].is_placed())
        self.assertTrue(self.my_room.furniturelist[1].is_placed())
        self.assertIsInstance(self.my_room, ro.Bedroom)

    def test_dining_room_algo(self):

        self.setup_a_room(1,1, ro.Dining_Room)
        chair = ri.Chair()
        stool = ri.Stool()
        self.my_room.set_furniturelist([chair,stool])
        self.my_room = self.my_generator.apply_algo(al.standard_dining_room(self.my_room))
        
        print(chair.get_location())
        print(stool.get_location())
        self.assertTrue(self.my_room.furniturelist[0].is_placed())
        self.assertTrue(self.my_room.furniturelist[1].is_placed())
        self.assertIsInstance(self.my_room, ro.Dining_Room)
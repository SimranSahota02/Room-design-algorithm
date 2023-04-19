import room_items as ri
import room_algos as al

class room:
  
    Base = None
    furniturelist = None
    name = ''
    
    def __init__(self, Base=None, furniturelist=None):
        
        if Base is None:
            self.Base = []
        else:
            self.Base = Base
        if furniturelist is None:
            self.furniturelist=[]
        else:
            self.furniturelist = furniturelist

    def get_room_name(self):
        return self.name
        
    def set_room_name(self, name):
        self.name = name

    def set_room_size(self, roomwidth, roomlength):

        self.Base = [[None for x in range(self.dims2cells(roomwidth))] for y in range(self.dims2cells(roomlength))]
        

    @staticmethod
    def cells2dims(cell_count):
        return (cell_count - 2)/2
    
    @staticmethod
    def dims2cells(dim):
        return int(dim * 2 + 2)

    def get_roomx(self):
        if len(self.Base) >0:
            return self.cells2dims( len(self.Base[0]) )
        else:
            return 0

    def get_roomy(self):
        return self.cells2dims( len(self.Base) )

    def get_room_dims(self):

        return int(self.get_roomx()), int(self.get_roomy())

    def get_room_dims_cells(self):
        
        if len(self.Base) > 0:
            return len(self.Base[0]), len(self.Base) #returns x,y
        else:
            return 0,0

    def collisions(self, itemx, itemy):  # takes in length and width of item

        found = True
        candidate_list = []

        for y in range(0, self.get_room_dims_cells()[1] - itemy ):  # for each location in the room

            for x in range(0, self.get_room_dims_cells()[0] - itemx ):
                found = True  # current location is valid

                for yy in range(0, itemy):  # for each location of the item

                    for xx in range(0, itemx):

                        if not self.check((x + xx),(y + yy)) or not found:  # if current location is not valid
                            found = False  # all locations in this loop are not valid

                        elif (yy == itemy - 1) and (xx == itemx - 1) and (found):
                            # if last item location and not yet invalid
                                candidate_list.append([x,y])

                        else:
                            pass  # current location is valid, next

        # for y in range(0, self.get_room_dims_cells()[1] - itemy ):  # for each location in the room

        #     for x in range(0, self.get_room_dims_cells()[0] - itemx ):
                

        #         for yy in range(0, itemy):  # for each location of the item

        #             for xx in range(0, itemx):

        #                 if not self.check((x + xx),(y + yy)):  # if current location is not valid
        #                     found = False  # all locations in this loop are not valid
        #                     break
        #                 else:
        #                     found = True  # current location is valid

        #             if found == False:
        #                 break

        #         if found == True:
        #             candidate_list.append([x,y])

        # print(candidate_list)
        return candidate_list

    def check(self, x, y):  # if this location is empty the fucntion returns a positive result
        if self.Base[y][x] is None:
            return True

        else:
            return False

    def add_to_furniturelist(self, furniture_item):

        self.furniturelist.append(furniture_item)

    def get_furniturelist(self):

        return self.furniturelist

    def set_furniturelist(self, new_list):

        self.furniturelist = new_list


    def place_furniture(self, furniture_item, locx, locy):

        for y in range(0, furniture_item.length):

            for x in range(0, furniture_item.width):

                self.Base[locy + y][locx + x] = furniture_item.__class__

        furniture_item.set_location(
            locx, locy
        )  # tell the furniture it's new coordinates

    def get_design_algos(self):
        return None

class Living_Room(room):
    def __init__(self):
        super().__init__()
        self.name = 'Living Room'
    
    def get_design_algos(self):
        return [al.standard_living_room]
        
class Study(room):
    def __init__(self):
        super().__init__()
        self.name = 'Study'

    def get_design_algos(self):
        return [al.standard_study]
        
class Kitchen(room):
    def __init__(self):
        super().__init__()
        self.name = 'Kitchen'

    def get_design_algos(self):
        return [al.standard_kitchen]
        
class Dining_Room(room):
    def __init__(self):
        super().__init__()
        self.name = 'Dining Room'

    def get_design_algos(self):
        return [al.standard_dining_room]
        
class Bedroom(room):
    def __init__(self):
        super().__init__()
        self.name = 'Bedroom'

    def get_design_algos(self):
        return [al.standard_bedroom]

# def test_no_candidates():  # given room 4x3 and 2x2 item at 1,0 when i check 4x2 item no candidates found
#     my_room = room()
#     my_room.set_room_size(4, 3)
#     my_table = ri.Furniture("Table", 2, 2)
#     my_room.place_furniture(my_table, 1, 0)
#     my_candidates = my_room.collisions(4, 2)
#     print(
#         "given room 4x3 and 2x2 item at 1,0 when i check 4x2 item no candidates found"
#     )
#     if len(my_candidates) == 0:
#         print("pass")
#     else:
#         print("fail")


# def test_empty_room_candidates():  # given room 5x5 when i check item 1x1 50 candidates found
#     my_room = room()
#     my_room.set_room_size(5, 5)
#     my_candidates = my_room.collisions(1, 1)
#     print("given room 5x5 when i check item 1x1 25 candidates found")
#     if len(my_candidates) == 50:
#         print("pass")
#     else:
#         print("fail")


# def test_small_room_candidates():  # given room 2x2 when i check item 3x1 no candidates found
#     my_room = room()
#     my_room.set_room_size(2, 2)
#     my_candidates = my_room.collisions(3, 1)
#     print("given room 2x2 when i check item 3x1 no candidates found")
#     if len(my_candidates) == 0:
#         print("pass")
#     else:
#         print("fail")


# if __name__ == "__main__":
#     test_no_candidates()
#     test_empty_room_candidates()
#     test_small_room_candidates()

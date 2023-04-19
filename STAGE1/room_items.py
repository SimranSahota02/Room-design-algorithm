import PIL.Image
import PIL.ImageTk  # for images of the item
import os  # for file/directory location


class room_item: 
    x = -1  # x and y are coords of tl corner of item when placed
    y = -1
    length = 0
    width = 0
    name = ""
    image_path = None

    def __init__(self, widthx=1, lengthy=1):

        self.length = lengthy
        self.width = widthx
        self.image_path = "resources/default.png"  # default

    def is_placed(self):

        if self.x != -1 and self.y != -1:
            return True

        else:
            return False

    def get_location(self):
        return self.x, self.y

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def get_dimy(self):

        return self.length

    def set_dimy(self, new_dim):

        self.length = new_dim

    def get_dimx(self):

        return self.width

    def set_dimx(self, new_dim):

        self.width = new_dim

    def get_name(self):

        return self.name

    def set_image_path(self, path):

        self.image_path = path

    # retun a reference to the image of this furniture item
    def get_image(self):

        # get the directory path of the current python file
        my_path = os.path.dirname(__file__)

        try:

            img = PIL.Image.open(
                my_path + os.path.sep + self.image_path
            )  # convert to readable format

        except FileNotFoundError:

            img = None

        return img  # still need to use PIL.ImageTk.PhotoImage to make it into a photo that can be drawn

    # returns a list of room item types that can replace this one on the room grid
    @staticmethod
    def can_replace_with(original_item):
        allowed = {
            Wall        : [Door, None],
            Door        : [Wall, None],
            Furniture   : [Furniture, None],
            None        : [Wall, Furniture]
        }

        return allowed[original_item]

class Wall(room_item):

    def __init__(self, widthx=1, lengthy=1):

        super().__init__(widthx, lengthy)


class Door(room_item):

    def __init__(self, widthx=1, lengthy=1):

        super().__init__(widthx, lengthy)



class Furniture (room_item):

    def __init__(self, name="Furniture", widthx=1, lengthy=1):

        self.name = name
        super().__init__(widthx, lengthy)



    # give a list of all available furniture types (used when choosing what furniture the user puts into the room)
    @staticmethod  # makes the method available on the class, not instances of the class
    def get_available_furniture_types():

        available_furniture = []
        available_furniture.append(("Lamp", Lamp))
        available_furniture.append(("Table", Table))
        available_furniture.append(("Kitchen table", Table))
        available_furniture.append(("Cofee table", Coffee_table))
        available_furniture.append(("Breakfast bar", Breakfast_bar))
        available_furniture.append(("Chair", Chair))
        available_furniture.append(("Armchair", Armchair))
        available_furniture.append(("Stool", Stool))
        available_furniture.append(("Sofa", Sofa))
        available_furniture.append(("Cabinet", Cabinet))
        available_furniture.append(("Bed", Bed))
        available_furniture.append(("Sink", Sink))
        available_furniture.append(("Oven", Oven))
        available_furniture.append(("Fridge", Fridge))
        available_furniture.append(("Dishwasher", Dishwasher))
        available_furniture.append(("Bin", Bin))
        available_furniture.append(("Dryer", Dryer))
        available_furniture.append(("Kitchen counter", Kitchen_counter))
        available_furniture.append(("Microwave", Microwave))
        available_furniture.append(("Bean bag", Bean_bag))
        available_furniture.append(("Vase", Vase))
        available_furniture.append(("TV", TV))

        return available_furniture


class Table(Furniture):
    def __init__(self, name="Table", widthx=2, lengthy=2):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/table_01.png"  # default

class Dining_table(Table):
    def __init__(self, name="Dining Table", widthx=4, lengthy=2):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/table_01.png"  # default

class Coffee_table(Furniture):
    def __init__(
        self, name="Coffee Table", widthx=2, lengthy=2,
    ):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/table_02.png"  # default

class Breakfast_bar(Furniture):
    def __init__(
        self, name="Breakfast bar", widthx=2, lengthy=2,
    ):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/table_02.png"  # default

class Lamp(Furniture):
    def __init__(self, name="Lamp", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/lamp_01.png"  # default


class Chair(Furniture):
    def __init__(self, name="Chair", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/chair_01.png"  # default

class Armchair(Furniture):
    def __init__(self, name="Armchair", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/chair_01.png"  # default

class Stool(Chair):
    def __init__(self, name="Stool", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/stool_01.png"  # default


class Sofa(Furniture):
    def __init__(self, name="Sofa", widthx=4, lengthy=2):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/sofa_01.png"  # default

class Cabinet(Furniture):
    def __init__(self, name="Cabinet", widthx=2, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/sofa_01.png"  # default

class Bed(Furniture):
    def __init__(self, name="Bed", widthx=4, lengthy=6):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/sofa_01.png"  # default

class Sink(Furniture):
    def __init__(self, name="Sink", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/sofa_01.png"  # default

class Oven(Furniture):
    def __init__(self, name="Oven", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/sofa_01.png"  # default

class Fridge(Furniture):
    def __init__(self, name="Fridge", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/sofa_01.png"  # default

class Dishwasher(Furniture):
    def __init__(self, name="Dishwasher", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/sofa_01.png"  # default

class Bin(Furniture):
    def __init__(self, name="Bin", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/sofa_01.png"  # default

class Dryer(Furniture):
    def __init__(self, name="Dryer", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/sofa_01.png"  # default

class Kitchen_counter(Cabinet):
    def __init__(self, name="Kitchen_counter", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/sofa_01.png"  # default

class TV(Furniture):
    def __init__(self, name="TV", widthx=4, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/tv_01.png"  # default

class Microwave(Furniture):
    def __init__(self, name="Microwave", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/table_01.png"  # default

class Bean_bag(Furniture):
    def __init__(self, name="Bean_bag", widthx=2, lengthy=2):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/table_01.png"  # default

class Vase(Furniture):
    def __init__(self, name="Vase", widthx=1, lengthy=1):

        super().__init__(name, widthx, lengthy)
        self.image_path = "resources/table_01.png"  # default

def test_furniture(furniture_item):
    print("Testing furniture: ", furniture_item.get_name())
    img = furniture_item.get_image()

    if img is not None:
        tkinter.Tk()
        photo = PIL.ImageTk.PhotoImage(img)
        print(furniture_item.get_name(), photo, photo.height(), photo.width())
    else:
        print("File not found")


if __name__ == "__main__":
    # test loading a dining_table_01
    import tkinter

    test_furniture(Furniture("default 3x1", 3, 1))
    test_furniture(Table("default table 3x1", 3, 1))
    test_furniture(Lamp("lamp 1x1", 1, 1))

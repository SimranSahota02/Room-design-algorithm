import python_array_test as at
import point_score as ps


# create a room
# get candidates for 1 item
# score candidates
# print best


def test_score_algorithm_1x1():  # With room size 1x1 and item 1x1 expect best coord 0,0
    my_room = at.room()
    my_room.set_room_size(1, 1)
    my_table = at.Furniture(1, 1, "Table")
    x = ps.best_place_for_item(my_table, my_room)
    if x[0] == 0 and x[1] == 0:
        print("Pass", x)
    else:
        print("Fail", x)


def test_score_algorithm_4x4():  # With room size 4x4 and item 2x1 at location 3,0 expect best coord 2,3 when placing item 1x2
    my_room = at.room()
    my_room.set_room_size(4, 4)
    my_chair = at.Furniture(2, 1, "Chair")
    my_room.place_furniture(my_chair, 3, 0)
    my_table = at.Furniture(1, 2, "Table")
    x = ps.best_place_for_item(my_table, my_room)
    if x[0] == 2 and x[1] == 3:
        print("Pass", x)
    else:
        print("Fail", x)


def test_room_dims():  # Given room size 1x5 room dimensions should be 1x5
    my_room = at.room()
    my_room.set_room_size(1, 5)
    print(my_room.get_room_dims()[0])
    print(my_room.get_room_dims()[1])


def test_place_two_items():  # Given room size 2x5 and furniture 1x1 and 1x1 idk they place at like 2,5 and 2,4
    my_room = at.room()
    my_room.set_room_size(5, 5)
    my_chair = at.Furniture(1, 1, "Chair")
    x = ps.best_place_for_item(my_chair, my_room)
    my_room.place_furniture(my_chair, x[0], x[1])
    my_table = at.Furniture(2, 1, "Table")
    y = ps.best_place_for_item(my_table, my_room)
    my_room.place_furniture(my_table, y[0], y[1])
    print(*my_room.Base, sep="\n")


if __name__ == "__main__":

    test_score_algorithm_1x1()
    test_score_algorithm_4x4()
    test_room_dims()
    test_place_two_items()

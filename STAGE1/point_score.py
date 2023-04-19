import python_array_test as at


# call score item for each coord
# return coord
# def best_place_for_item(furniture_item, room_design):
#     my_candidates = room_design.collisions(
#         furniture_item.get_dimx(), furniture_item.get_dimy()
#     )
#     best_score = []
#     best_coord = []

#     for i in range(0, len(my_candidates)):

#         this_score = score_item(furniture_item, my_candidates[i], room_design)

#         if this_score >= best_score:

#             best_coord.append(my_candidates[i]) 
#         else:
#             pass

#     return best_coord


def score_item(furniture_item, my_candidate, room_design):
    score = float(0)  # reset score and define as a float
    score += 100  # p1 add 100 pts
    empty = 0  # p1 set counter to 0

    for j in range(
        0, int(furniture_item.get_dimy())
    ):  # p1 for each location vertically the item takes up

        for i in range(
            0, room_design.get_room_dims()[0]
        ):  # p1 for each location in the room horizontal to this location

            if (
                room_design.Base[my_candidate[1] + j][i] == 0
            ):  # p1 if said location is empty, add to the counter
                empty += 1
            else:
                pass

    score -= 100 // empty  # p1 subtract a percentage of 100pts for each empty location

    # print(score)
    return score

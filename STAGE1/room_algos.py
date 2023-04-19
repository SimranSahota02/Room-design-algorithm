import random
import copy
import point_score as ps
import python_array_test as at
import room_items as ri 
# takes a room, algo
class design_generator:
    room = None
    algo = None

    def __init__(self, room):
        self.room = room
    
    # for each furniture item
    # find the best cell
    # if multiple, ask the algo which to use
    def apply_algo(self, algo):
        self.algo = algo

        # create a new room obj from the initial room
        my_new_design = copy.deepcopy(self.room)

        # for each furniture item
        for this_item in my_new_design.get_furniturelist():

            # find candidates (collisions)
            # for each candidate
            # get score for candidate using algo
            # pick candidate with best score
            # if all have same score then use algo.pick best coords for mathching score
            coord_to_place = self.algo.best_place_for_item(this_item,my_new_design)
            if len(coord_to_place) > 1:
                coord_to_place = self.algo.decide_between_matching_scores(coord_to_place, this_item) #this selects the best coordinate 
                my_new_design.place_furniture(this_item, coord_to_place[0], coord_to_place[1])
            elif len(coord_to_place) == 0:
                pass
            else:
                my_new_design.place_furniture(this_item, coord_to_place[0][0], coord_to_place[0][1])

            # place item into candidate with best score
            
        return my_new_design 

class design_algo:
    methods = [] #scoring methods for this algo
    name = ''
    room = None

    def __init__(self, room):
        self.room = room
    
    def get_name(self):
        return self.name

    # apply each method to the cell, add the score for each method to get total score for that cell
    def score_cell( self, room , x, y, item):

        cell_score = 0

        for method in self.methods:
            
            cell_score = cell_score + method.score_cell( self.room, x, y, item )

        return cell_score

    #find the best location for the item by finding its candidates then scoring it
    def best_place_for_item(self, furniture_item, room_design):

        my_candidates = room_design.collisions(
        furniture_item.get_dimx(), furniture_item.get_dimy()
        )
        best_score = [0]
        best_coord = []

        for i in range(0, len(my_candidates)):
            #score one candidate
            this_score = self.score_cell( room_design, my_candidates[i][0], my_candidates[i][1], furniture_item)
            #intent: keep coords with the best scores
            #if new score is equal to old score append score and candidate to best lists
            #if new score is greater than old score reinitialise best lists, append new score and candidate
            if this_score == best_score[-1]:

                best_score.append(this_score)    
                best_coord.append(my_candidates[i]) 
            elif this_score > best_score[-1]:

                best_score = []
                best_coord = []
                best_score.append(this_score)    
                best_coord.append(my_candidates[i])

            else:
                pass #ignore lower score
        
        return best_coord
    
    def decide_between_matching_scores(self, cells_with_matching_scores, item):
        return cells_with_matching_scores[0] # always choose the first #TODO something cleverer

class random_design(design_algo):
    def __init__(self, room):

        super().__init__(room)
        self.name = 'Random'
        self.methods.append(random_score())

    def decide_between_matching_scores(self, cells_with_matching_scores, item):
        return cells_with_matching_scores[ random.randint(0, len(cells_with_matching_scores)-1) ]

class standard_kitchen(design_algo):

    def __init__(self, room):

        super().__init__(room)
        self.name = 'Standard kitchen'
        self.methods.append(along_wall())
        self.methods.append(Sink_oven_fridge())
        self.methods.append(door_space())
        self.methods.append(Tables_by_chairs())

    def decide_between_matching_scores(self, cells_with_matching_scores, item):
        return cells_with_matching_scores[ random.randint(0, len(cells_with_matching_scores)-1) ]
        
class standard_study(design_algo):

    def __init__(self, room):

        super().__init__(room)
        self.name = 'Standard study'
        self.methods.append(along_wall())
        self.methods.append(parallel_to_longest_wall())
        self.methods.append(door_space())
        self.methods.append(Tables_by_chairs())

    def decide_between_matching_scores(self, cells_with_matching_scores, item):
        return cells_with_matching_scores[ random.randint(0, len(cells_with_matching_scores)-1) ]

class standard_living_room(design_algo):

    def __init__(self, room):

        super().__init__(room)
        self.name = 'Standard living room'
        self.methods.append(TV_inline_with_sofa)
        self.methods.append(parallel_to_longest_wall())
        self.methods.append(door_space())
        self.methods.append(Tables_by_chairs())

    def decide_between_matching_scores(self, cells_with_matching_scores, item):
        return cells_with_matching_scores[ random.randint(0, len(cells_with_matching_scores)-1) ]

class standard_dining_room(design_algo):

    def __init__(self, room):

        super().__init__(room)
        self.name = 'Standard dining room'
        self.methods.append(next_to_space())
        self.methods.append(table_in_centre())
        self.methods.append(door_space())
        self.methods.append(Tables_by_chairs())

    def decide_between_matching_scores(self, cells_with_matching_scores, item):
        return cells_with_matching_scores[ random.randint(0, len(cells_with_matching_scores)-1) ]

class standard_bedroom(design_algo):

    def __init__(self, room):

        super().__init__(room)
        self.name = 'Standard bedroom'
        self.methods.append(along_wall())
        self.methods.append(parallel_to_longest_wall())
        self.methods.append(door_space())
        self.methods.append(bed_in_centre())

    def decide_between_matching_scores(self, cells_with_matching_scores, item):
        return cells_with_matching_scores[ random.randint(0, len(cells_with_matching_scores)-1) ]

class scoring_method:
    name = ''

    def score_cell( self, room, x, y, furniture_item):
        return None

class same_score_for_all(scoring_method):

    def __init__(self):
        self.name = 'Same score for all cells'
        super().__init__()

    def score_cell( self, room, x, y, furniture_item):
        #room.Base[y][x]
        return 100
    
class only_0_0(scoring_method):

    def __init__(self):
        self.name = 'Only top left'
        super().__init__()

    def score_cell( self, room, x, y, furniture_item):
        if x==0 and y == 0:
            return 100
        else:
            return 0

class random_score(scoring_method):

    def __init__(self):
        self.name = 'Random'
        super().__init__()

    def score_cell( self, room, x, y, furniture_item):
        score_to_add = random.randint(0,100)
        return score_to_add
    
class along_wall(scoring_method):

    def __init__(self):
        self.name = 'Along wall'
        super().__init__()

    def score_cell( self, room, x, y, furniture_item):
        score_to_add = int(0)
        for locx in range(x - 1, x + furniture_item.get_dimx() + 1):
                    for locy in range(y - 1, y + furniture_item.get_dimy() + 1):
                        #set a score if found -- otherwise function will use defualt 0 value
                        if room.Base[locx][locy] == ri.Wall():
                            score_to_add += int(100)
                        else:
                            pass

        return score_to_add

class next_to_space(scoring_method):
    
    def __init__(self):
        self.name = 'In space'
        super().__init__()

    def score_cell( self, room, x, y, furniture_item):
        score_to_add = int(0)
        for locx in range(x - 1, x + int(furniture_item.get_dimx()) + 1):
                    for locy in range(y - 1, y + furniture_item.get_dimy() + 1):
                        
                        if room.Base[locx][locy] is None:
                            score_to_add += int(100)
                        else:
                            pass
        
        return score_to_add

class parallel_to_longest_wall(scoring_method):

    def __init__(self):
        self.name = 'Along longest wall'
        super().__init__()

    def score_cell( self, room, x, y, furniture_item):
        score_to_add = int(0)
        if room.get_room_dims_cells[0] >= room.get_room_dims_cells()[1]:
            for locy in range(y - 1, y + furniture_item.get_dimy() + 1):

                    if room.Base[locy][room.get_room_dims_cells[1]] is ri.Wall:
                        score_to_add = int(100)
                    else:
                        pass 
        else:
            for locx in range(x - 1, x + furniture_item.get_dimx() + 1):

                    if room.Base[room.get_room_dims_cells()[0]][locx] is ri.Wall:
                        score_to_add = int(100)
                    else:
                        pass 
        
        return score_to_add

class door_space(scoring_method): 

    def __init__(self):
        self.name = 'Allow door space'
        super().__init__()

    def score_cell( self, room, x, y, furniture_item):
        score_to_add = int(0)
        for locx in range(x - 1, x + furniture_item.get_dimx() + 1):
                for locy in range(y - 1, y + furniture_item.get_dimy() + 1):

                    #set a score if found -- otherwise function will use defualt 0 value
                    if room.Base[locy][locx] == ri.Door:
                        score_to_add = int(-100)

                    else:
                        pass

        return score_to_add

class TV_inline_with_sofa(scoring_method):
    
    def __init__(self):
        super().__init__()
        self.name = 'Set TV and sofa'

    #find locations not diagonal to item that contain 
    def score_cell( self, room, x, y, furniture_item):
        score_to_add = int(0)
        if furniture_item == ri.Sofa or furniture_item == ri.TV:
            
            if furniture_item == ri.Sofa:
                set_item = ri.TV
            else:
                set_item = ri.Sofa

            for locx in range(0, room.get_room_dims_cells()[0]):
                for locy in range(y - 1, y + furniture_item.get_dimy() + 1):
                    #set a score if found -- otherwise function will use defualt 0 value
                    if room.Base[locy][locx] == set_item:
                        score_to_add = int(100)
                    else:
                        pass
            for locx in range(x - 1, x + furniture_item.get_dimx() + 1):
                for locy in range(0, room.get_room_dims_cells()[1]):
                    #set a score if found -- otherwise function will use defualt 0 value
                    if room.Base[locy][locx] == set_item:
                        score_to_add = int(100)
                    else:
                        pass
        else:
            pass                
        return score_to_add

class table_in_centre(scoring_method):
    
    def __init__(self):
        super().__init__()
        self.name = 'Table in centre'

    #find locations around item that are room centre
    def score_cell( self, room, x, y, furniture_item):
        score_to_add = int(0)
        if furniture_item == ri.Table:
            for locx in range(x - 1, x + furniture_item.get_dimx() + 1):
                for locy in range(0, room.get_room_dims_cells()[1]):
                    if room.Base[locy][locx] == room.Base[room.get_room_dims_cells()[0] /2 ][room.get_room_dims_cells()[1]/2]:
                        score_to_add = int(200)

        return score_to_add

class bed_in_centre(scoring_method):
    
    def __init__(self):
        super().__init__()
        self.name = 'Table in centre'

    #find locations around item that are room centre
    def score_cell( self, room, x, y, furniture_item):
        score_to_add = int(0)
        if furniture_item == ri.Bed:
            for locx in range(x - 1, x + furniture_item.get_dimx() + 1):
                for locy in range(0, room.get_room_dims_cells()[1]):
                    if room.Base[locy][locx] == room.Base[room.get_room_dims_cells()[0] /2 ][room.get_room_dims_cells()[1]/2]:
                        score_to_add = int(200)

        return score_to_add
class Tables_by_chairs(scoring_method):
    
    def __init__(self):
        super().__init__()
        self.name = 'Set chairs and tables'
    #find adjacent locations with the set item in them, add 100 if found
    def score_cell( self, room, x, y, furniture_item):
        score_to_add = int(0)
        if furniture_item == ri.Chair or furniture_item == ri.Table:
            
            if furniture_item == ri.Chair:
                set_item = ri.Table
            else:
                set_item = ri.Chair
            #from top-leftmost position next to item to bottom-rightmost position next to item
            for locx in range(x - 1, x + furniture_item.get_dimx() + 1):
                for locy in range(y - 1, y + furniture_item.get_dimy() + 1):
                    #set a score if found -- otherwise function will use defualt 0 value
                    if room.Base[locy][locx] == set_item:
                        score_to_add = int(100)
                    else:
                        pass
        else:
            pass                
        return score_to_add

class Sink_oven_fridge(scoring_method):
    
    def __init__(self):
        super().__init__()
        self.name = 'Sink oven and fridge triangle'

    def score_cell( self, room, x, y, furniture_item):
        score_to_add = int(0)
        if furniture_item == ri.Sink or furniture_item == ri.Oven or furniture_item == ri.Fridge:
            
            if furniture_item == ri.Sink:
                set_item_0 = ri.Oven
                set_item_1 = ri.Fridge
            elif furniture_item == ri.Oven:
                set_item_0 = ri.Sink
                set_item_1 = ri.Fridge
            else:
                set_item_0 = ri.Oven
                set_item_1 = ri.Sink
            
            #for each location within 2.5metres of the item
            found = None
            for locx in range(x - 5, x + furniture_item.get_dimx + 5):
                for locy in range(y - 5, y + furniture_item.get_dimy + 5):
                    
                    if found == None:
                        if room.Base[locy][locx] == set_item_0:
                            found = "item_0"
                            score_to_add = int(100)
                        
                        if room.Base[locy][locx] == set_item_1:
                            found = "item_1"
                            score_to_add = int(100)
                    
                    elif found == "item_0":
                        if room.Base[locy][locx] == set_item_1:
                            score_to_add = int(200)
                            found = "both"

                    elif found == "item_1":
                        if room.Base[locy][locx] == set_item_0:
                            score_to_add = int(200)
                            found = "both"
                    
                    elif found == "both":
                        pass

        return score_to_add    

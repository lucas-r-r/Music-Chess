import Chess
import random

def pawn_mode_generator(pawns_coords, color = "white"):
    coeficients = [1, 2, 2, 5, 7, 10, 10, 11]
    linear_correction = [0, 0, -1, 0, 0, 1, 0, 0]
    number_of_pawns = len(pawns_coords)
    pitches_list = set()
    for i in range(number_of_pawns):

        #print("coeficient is ", coeficients[pawns_coords[i][0]], "and y coord is", pawns_coords[i][1])
        if pawns_coords[i][1] == 1:
            linear_correction_single = 0
        else:
            linear_correction_single = linear_correction[pawns_coords[i][0]]
        pitch = (coeficients[pawns_coords[i][0]] * (pawns_coords[i][1]-1) + linear_correction_single ) % 12 + 60 # add later random 3-5 * 12
        if (pitch % 12) != 0:
            while (pitch in pitches_list):
                pitch = (pitch + 5) % 12 + 60
        print("Pitch to be added to mode:", pitch)
        #input("enter to continue")
        pitches_list.add(pitch)

    return pitches_list

def pawn_advance(pawns_coords, color = "white"):
    number_of_pawns = len(pawns_coords)
    total = 0
    for i in range(number_of_pawns):
        total += pawns_coords[i][1]-1
    print(f"Pawn advance count is {total} for {color}")
    return total
print(pawn_mode_generator([[0,1],[1, 1],[2, 3],[3,4],[4,2],[5,1],[6,3],[7,1]]))

def get_piece_type_positions(piece_type, color):
    if color == "white":
        #print("color is white")
        color = Chess.a_game.white
    else:
        color = Chess.a_game.black
    return Chess.a_game.get_piece_type_positions(piece_type, color)

def pop_set(the_set):
    if len(the_set) == 0:
        return [False]

    l = list(the_set)
    popped = l.pop(random.randrange(len(l)))
    new_set = set(l)

    return [new_set, popped]

class Mode():


    def __init__(self, mode, color = None):
        self.mode = mode
        self.next_mode = set()
        self.notes_to_dissappear = set()
        self.notes_to_play_next = set()
        self.color = color
        self.transposition = 0

    def clear_mode(self):
        self.next_mode = set()
        self.mode = set()

    def receive_next_mode(self, next_mode):
        self.next_mode = next_mode
        self.notes_to_dissappear = self.get_notes_to_dissappear(next_mode)
        print(f"Notes to remove next for {self.color}, {self.notes_to_dissappear}")
        self.notes_to_play_next = self.get_notes_to_play_next(next_mode)
        print(f"Notes to play next for {self.color}, {self.notes_to_play_next}")

    def add_note(self):
        popping = pop_set(self.notes_to_play_next)
        if popping[0] == False:
            return False
        else:

            self.notes_to_play_next = popping[0]
            note = popping[1]
            print("add", note)
            #note = self.notes_to_play_next.pop()
            self.mode.add(note)
            return note


    def remove_note(self):

        try:
            popping = pop_set(self.notes_to_dissappear)
            if popping[0] == False:
                return False
            else:

                self.notes_to_dissappear = popping[0]
                note = popping[1]
                print("remove", note)
                #note = self.notes_to_play_next.pop()
                self.mode.remove(note)
                return note
        except KeyError as e:
            print("No note to remove")
            return False


    def get_notes_to_dissappear(self, next_mode):
        notes_to_dissappear = self.mode - next_mode
        return notes_to_dissappear
    def get_notes_to_play_next(self, next_mode):
        notes_to_play_next = next_mode - self.mode
        return notes_to_play_next





    def get(self):
        return Mode



white_mode = Mode(set(), "white")
black_mode = Mode(set(), "black")
def test_code():
    current_mode = {5, 2, 3, 11, 6, 4}
    next_mode = {2, 4, 5, 10, 9}
    print(f"passing from {current_mode} to {next_mode}")
    white_mode.receive_next_mode(next_mode)
    print(f"{white_mode.mode} is set to become {white_mode.next_mode}")

    while True:
        action = input("Add or remove note (A/R)")
        if action == "a":
            note = white_mode.add_note()
            if note != False:
                print(f"{note} added. Playing {white_mode.mode}")
            else:
                print("No note to add")
        if action == "r":
            note = white_mode.remove_note()

            if note != False:
                print(f"{note} removed. Playing {white_mode.mode}")
            else:
                print("No note to remove")

#test_code()

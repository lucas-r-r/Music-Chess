import sys
from common import vprint

verbose = False


FEN_to_piece_type = {'1': ['blank space', 'blank space'],
                    'K': ['King', 'White'],
                    'Q': ['Queen', 'White'],
                    'R': ['Rook', 'White'],
                    'B': ['Bishop', 'White'],
                    'N': ['Knight', 'White'],
                    'P': ['Pawn', 'White'],
                    'k': ['King', 'Black'],
                    'q': ['Queen', 'Black'],
                    'r': ['Rook', 'Black'],
                    'n': ['Knight', 'Black'],
                    'b': ['Bishop', 'Black'],
                    'p': ['Pawn', 'Black']}

                    #It might be useful to take the shortcut and create the class directly with the dictionary, if that's possible.
file_to_x = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
x_to_file = {"a", "b", "c", "d", "e", "f", "g", "h"}

# Piece_to_FEN = { None: '1',
#                 ['King', 'White']: 'K',
#                 ['Queen', 'White']: 'Q',
#                 ['Rook', 'White']: 'R',
#                 ['Bishop', 'White']: 'B',
#                 ['Knight', 'White']: 'N',
#                 ['Pawn', 'White']: 'P',
#                 ['King', 'Black']: 'k',
#                 ['Queen', 'Black']: 'q',
#                 ['Rook', 'Black']: 'r',
#                 ['Knight', 'Black']: 'n',
#                 ['Bishop', 'Black']: 'b',
#                 ['Pawn', 'Black']: 'p'
#
#                 }





def print_illegal_move(cause):
    print(f"Illegal move: {cause}")




def coordinate_to_number(coordinate):
    a =[file_to_x[coordinate[0]], rank_to_y(coordinate[1])]
    print(f"{coordinate} converted to {a}")
    return a





def rank_to_y(rank):
    return abs(int(rank) - 8)

def y_to_rank(y):
    return abs(y-8)

def substitute_FEN_numbers(FEN_coordinates):
    """Substitute the number in FEN coordinates with that number of 1s"""
    return FEN_coordinates.replace('8', '1' * 8).replace('7', '1' * 7).replace('6', '1' * 6).replace('5', '1' * 5).replace('4', '1' * 4).replace('3', '1' * 3).replace('2', '1' * 2).replace('/', '')

def open_FEN_file():
    False

class Piece():
    list_of_pieces = []
    def __init__(self, color, position):
        self.color = color
        #self.piece_type = piece_type
        self.has_moved = False
        self.move_count = 0
        self.position = position
        self.index = len(Piece.list_of_pieces)
        Piece.list_of_pieces.append(self)
        self.color_index = len(self.color.list_of_pieces)
        self.color.list_of_pieces.append(self)
        print(f"Piece index is {self.index}")
        print(f"Piece index in color {self.color.name} is {self.color_index}")

    def get_alive_pieces(color = "both"):
        alive_pieces = []
        if color == "both":
            for piece in Piece.list_of_pieces:
                if piece.position != [-1, -1]:
                    alive_pieces.append(piece)
        else:
            for piece in Piece.list_of_pieces:
                if piece.position != [-1, -1] and piece.color == color:
                    alive_pieces.append(piece)
        return alive_pieces




    def get_relative_rank(self):
        rel_rank = self.position[1]
        if self.color == self.color.game.white and self.position[1] != -1:
            return abs(rel_rank-7)
        else:
            return rel_rank

    def get_piece_info_string(self, rel_pos = True):
        info = []
        info.append(self.color.name)
        info.append(str(self.color_index))

        piece_type = self.name
        if piece_type == "Bishop":
            piece_type += self.get_square().scolor
        info.append(piece_type)

        info.append(str(self.position[0]))
        info.append(str(self.get_relative_rank()))
        info.append(str(self.move_count))
        the_string = " ".join(info)
        return the_string

    def get_symbol(self):
        return chr(ord(self.symbol) + self.color.char_modifier)
    def move_eval(self, dest_position, turn_aware = True):
        print("Piece type or its move is not defined, so there's no possible move.")
        print("We'll asume your move is legal")
        return [True, None]
    def do_move(self, dest_position, special):
        destination_piece = a_game.chessboard[dest_position[0]][dest_position[1]].get_piece()
        if destination_piece != None:
            a_game.capture(dest_position)
        if special[0] == "en passant":
            a_game.en_passant = special[1]
        else:
            if special[0] == "capture en passant":
                if a_game.en_passant[1] == 2:
                    print("capturing en passant a black pawn")
                    a_game.capture([dest_position[0],3])
                elif a_game.en_passant[1] == 6:
                    print("capturing en passant a white pawn")
                    a_game.capture([dest_position[0],4])
                else:
                    raise Exception("There's no valid en passant 'y' coordinate stored in memory")
            elif special[0] == "Castling kingside":
                rook_position = self.color.the_Rook_K.position
                self.color.the_Rook_K.position = [rook_position[0]-2, rook_position[1]]
            elif special[0] == "Castling queenside":
                rook_position = self.color.the_Rook_Q.position
                self.color.the_Rook_Q.position = [rook_position[0]+3, rook_position[1]]
            elif special[0] == "Promotion":
                if a_game.promotion_choice == 0:
                    Piece.list_of_pieces[self.index] = Queen(self.color, dest_position)
                elif a_game.promotion_choice == 1:
                    Piece.list_of_pieces[self.index] = Rook(self.color, dest_position)
                elif a_game.promotion_choice == 2:
                    Piece.list_of_pieces[self.index] = Bishop(self.color, dest_position)
                elif a_game.promotion_choice == 3:
                    Piece.list_of_pieces[self.index] = Knight(self.color, dest_position)

            print("Erasing en passant information")
            a_game.en_passant = None
        # if a_game.chessboard[dest_position[0]][dest_position[1]].get_piece():
        #     self.capture(dest_position)

        self.position = dest_position
        self.has_moved = True
        self.move_count += 1
        a_game.next_turn()
        print(f"{self.color.name} {self.name} moved. Turn for {a_game.turn}.")
    def get_square(self):
        #Uses a function to get the square of an specific piece.
        return a_game.chessboard[self.position[0]][self.position[1]]
    def destination_is_same_color(self, destination):
        try:
            if self.color == a_game.chessboard[destination[0]][destination[1]].get_piece().color:
                return True
            else:
                return False
        except AttributeError:
            print("No piece in destination")


class King(Piece):
    name = 'King'
    symbol = '♔'
    letter = "K"
    value = 0
    def __init__(self, color, position):
        super().__init__(color, position)
        self.color.the_King = self
    def move_eval(self, dest_position, turn_aware = True):
        def is_castling_K():
            if oy == dy and dx - ox == 2 and self.color.the_King.has_moved == False and self.color.the_Rook_K.has_moved == False:
                return True
            else:
                return False
        def is_castling_Q():
            if oy == dy and dx - ox == -2 and self.color.the_King.has_moved == False and self.color.the_Rook_Q.has_moved == False:
                return True
            else:
                return False
        ox = self.position[0]
        oy = self.position[1]
        dx = dest_position[0]
        dy = dest_position[1]
        dest_piece = a_game.chessboard[dx][dy].get_piece()
        print(f"Evaluating a {self.color. name} {self.name}")
        if (abs(dx - ox) <= 1) and abs(dy-oy) <= 1:
            if self.destination_is_same_color(dest_position):
                print("There's a piece of the same color in destination")
                return [False]

            else:
                return [True, None]
        elif is_castling_K() == True:
            return [True, "Castling kingside"]
        elif is_castling_Q() == True:
            return [True, "Castling queenside"]
        else:
            print_illegal_move("King can only move by one square, except in castling")
            return [False]


class Queen(Piece):
    name = 'Queen'
    symbol = '♕'
    letter = 'Q'
    value = 9
    def move_eval(self, dest_position):
        if Rook.move_eval(self, dest_position)[0] == True:
            print("Queen moved horizontally")
            return [True, None]

        elif Bishop.move_eval(self, dest_position)[0] == True:
            print("Queen moved diagonally")
            return [True, None]
        else:
            return [False]
class Rook(Piece):
    name = 'Rook'
    symbol = '♖'
    letter = 'R'
    value = 5
    def __init__(self, color, position):

        super().__init__(color, position)
        if self.position[0] == 0:
            self.color.the_Rook_Q = self
        elif self.position[0] == 7:
            self.color.the_Rook_K = self
    def move_eval(self, dest_position):
        def are_pieces_on_the_way():
            if abs(delta) == 1:
                print("Rook is only moving by one square")
                return False
            if delta < 0:
                orientation = -1
            else:
                orientation = 1
            print(f"orientation is {orientation}")
            print(direction)
            if direction == "H":
                for i in range(1, abs(delta)):
                    print(f"evaluating an horizontal move of {i} squares")
                    piece = a_game.chessboard[ox + (i * orientation)][oy].get_piece()
                    if piece != None:
                        return True
                return False
            elif direction == "V":
                for i in range(1, abs(delta)):
                    print(f"evaluating a vertical move of {i} squares")
                    piece = a_game.chessboard[ox][oy + (i * orientation)].get_piece()
                    if piece != None:
                        return True
                return False
        ox = self.position[0]
        oy = self.position[1]
        dx = dest_position[0]
        dy = dest_position[1]
        dest_piece = a_game.chessboard[dx][dy].get_piece()
        print(f"Evaluationg a {self.color. name} {self.name}")
        if ox != dx and oy != dy:
            print_illegal_move("Rooks can only move horizontally or vertically")
            return [False]
        elif oy == dy:
            print("Rook is going to move horizontally")
            direction = "H"
            delta = dx - ox
        elif ox == dx:
            print("Rook is going to move vertically")
            direction = "V"
            delta = dy - oy
        else:
            raise Exception("move should be either horizontal or vertical!")
        vprint(f"number of squares the rook is displacing: {delta}")
        if are_pieces_on_the_way():
            print_illegal_move("There are pieces on the way and rook can't move")
            return [False]
        else:
            print("There aren't pieces on the way")
        if self.destination_is_same_color(dest_position):
            print("There's a piece of the same color in destination")
            return [False]
        return [True, None]

class Bishop(Piece):
    name = 'Bishop'
    symbol = '♗'
    letter = 'B'
    value = 3

    def move_eval(self, dest_position):
        def are_pieces_on_the_way():
            delta = abs(dx - ox)

            #getting move directions
            if ox < dx:
                orientationH = 1
            else:
                orientationH = -1
            if oy < dy:
                orientationV = 1
            else:
                orientationV = -1

            vprint(f"Delta movement: {delta}. Orientation H: {orientationH}. Orientation V: {orientationV}")
            if abs(delta) == 1:
                print("Bishop is only moving by one square")
                return False
            else:
                for i in range(1, delta):
                    #print(f"i value is {i}")
                    if a_game.chessboard[ox + (i * orientationH)][oy + (i * orientationV)].get_piece() != None:
                        print("Found piece on the way")
                        return True
                return False

        ox = self.position[0]
        oy = self.position[1]
        dx = dest_position[0]
        dy = dest_position[1]
        dest_piece = a_game.chessboard[dx][dy].get_piece()
        if (abs(ox-dx) != abs(oy-dy)):
            print_illegal_move("Bishops must move diagonally")
            return [False]
        else:

            if are_pieces_on_the_way():
                print_illegal_move("There are pieces on the way and bishop can't move")
                return [False]
            if self.destination_is_same_color(dest_position):
                print("There's a piece of the same color in destination")
                return [False]
            return [True, None]

class Knight(Piece):
    name = 'Knight'
    symbol = '♘'
    letter = 'N'
    value = 3

    def move_eval(self, dest_position):
        ox = self.position[0]
        oy = self.position[1]
        dx = dest_position[0]
        dy = dest_position[1]
        deltaX = dx - ox
        deltaY = dy - oy
        if (((abs(deltaX) == 2) and (abs(deltaY) == 1)) or (abs(deltaX) == 1 and (abs(deltaY) == 2))):
            if self.destination_is_same_color(dest_position):
                print("There's a piece of the same color in destination")
                return [False]
            return [True, None]
        else:
            print_illegal_move("That's not a standard knight move")
            return [False]

class Pawn(Piece):
    name = 'Pawn'
    symbol = '♙'
    letter = 'P'
    value = 1
    #Need to rename this to uppercase, to match conventions.
    def __init__(self, color, position):
        super().__init__(color, position)
        self.x = 1 #???? Try to erase this and see if it breaks!
        self.has_moved = False
    def move_eval(self, dest_position):
        #set variable names more usable
        ox = self.position[0]
        oy = self.position[1]
        dx = dest_position[0]
        dy = dest_position[1]
        #None = dest_position[2]
        dest_piece = a_game.chessboard[dx][dy].get_piece()
        print(f"Evaluating a {self.color. name} {self.name}")
        #if not (dy == 0 or dy == 7):
        #    None = None

        if (self.color == a_game.white and oy - 1 == dy) or (self.color == a_game.black and oy + 1 == dy):
            if ox == dx:
                if a_game.chessboard[dx][dy].get_piece() == None: #determine wether there is a piece present
                    print("moving pawn one forward")
                    print(f"relative rank is {a_game.get_relative_rank(dy, self.color)}")
                    if a_game.get_relative_rank(dy, self.color) == 7:
                        print("Pawn will promote!")
                        return [True, "Promotion"]
                    else:
                        return [True, None]
                else:
                    print_illegal_move("There's a piece present in the destination square")
                    return [False, None]

            elif ((ox == dx+1) or (ox == dx-1)): #determine if a capture is possible
                if dest_piece == None:
                    if a_game.en_passant != None:
                        if a_game.en_passant == dest_position:

                            print("capturing en passant")
                            return [True, "capture en passant"]
                    else:
                        print_illegal_move("there's no piece to capture when moving diagonally")
                        return [False, None]
                else:
                    print("this is a valid capture move")
                    if a_game.get_relative_rank(dy, self.color) == 7:
                        print("Pawn will promote!")
                        return [True, "Promotion"]
                    else:
                        return [True, None]

        elif (     ((self.color == a_game.white #determine if initial move can be done
                            and oy - 2 == dy)
                       or (self.color == a_game.black
                            and oy + 2 == dy)) #moves two squares forward
                   and ox == dx #file is the same
                   and self.has_moved == False #hasn't moved yet
                   and (self.color == a_game.white
                          and (a_game.chessboard[dx][oy - 1].get_piece() == None)
                        or (self.color == a_game.black
                          and (a_game.chessboard[dx][oy + 1].get_piece() == None)))): #there's no piece in between
            if dest_piece == None:

                if self.color == a_game.white:
                    en_passant = [dx, dy + 1]
                elif self.color == a_game.black:
                    en_passant = [dx, dy - 1]
                else:
                    print("Error, there should be an en passant assignment")
                print(f"initial two squares move, en passant set to {en_passant}")
                return [True, "en passant", en_passant]
            else:
                print_illegal_move("Pawn can't perform two square initial move because there's a piece present in destination")
                return [False]

        else:
            print_illegal_move("that's not a standard pawn move")
            return [False]
        print("move not implemented, you shouldn't actually see this message")
class Player():
    def __init__(self, color, char_modifier, game = None):
        self.name = color
        self.char_modifier = char_modifier
        self.can_castle_K = True
        self.can_castle_Q = True
        self.the_King = None
        self.the_Rook_K = None
        self.the_Rook_Q = None
        self.list_of_pieces = []
        self.game = game

    def is_same_color(self, other_piece):
        if other_piece.color == self.color:
            return True
        else:
            return False

    def the_other_player(self):
        if self == White:
            return Black
        elif self == Black:
            return White
        else:
            raise Exception("The player does not exist")


class Square(object):
    def __init__(self, position):
        self.position = position
        #substitute this with get_piece()
        self.piece = None
        if (position[0] + position[1]) % 2 == 1:
            self.scolor = "D"
        else:
            self.scolor = "L"


    def get_piece(self):
        #obtains the corresponding piece in the square, or returns "None" if none is present.
        for piece in Piece.get_alive_pieces():
            #print(f"Position of piece, {piece.position}. Position of square: {self.position}")
            if piece.position == self.position:
                #print("found piece. Yay!")
                return piece
            else:
                pass

        return None

def assign_piece(piece, position):
    p = FEN_to_piece_type[piece]
    if p[1] == 'White':
        c = a_game.white
    elif p[1] == 'Black':
        c = a_game.black
    else:
        c = ''
    if p[0] == 'Queen':
        return Queen(c, position)
    elif p[0] == 'King':
        return King(c, position)
    elif p[0] == 'Rook':
        return Rook(c, position)
    elif p[0] == 'Bishop':
        return Bishop(c, position)
    elif p[0] == 'Knight':
        return Knight(c, position)
    elif p[0] == 'Pawn':
        return Pawn(c, position)
    else:
        return None





class Game():
    def __init__(self):
        #Create players
        self.white = Player('white', 0, self)
        self.black = Player('black', 6, self)
        self.turn = self.white
        self.half_move = 0
        self.move = 1
        self.chessboard = [[Square([i, j]) for j in range(8)] for i in range(8)] #rever como se fan os putos geradores!!!
        self.en_passant = None
        self.promotion_choice = 0

    def init_game(self, FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        """Initializes the game state, with a standard start as default"""
        Piece.list_of_pieces = []
        self.white.list_of_pieces = []
        self.black.list_of_pieces = []
        self.move = 1 #still need to get it from FEN
        if open_FEN_file():
            pass
        print('Input FEN:', FEN)
        #slice part of coordinates
        if verbose == True:
            print('Extracting FEN coordinates...')
        turn_division = FEN.index(' ')

        #process the coordinates part
        FEN_coordinates = FEN[0:turn_division]
        #substitute numbers for 'n' number of 1
        FEN_coordinates = substitute_FEN_numbers(FEN_coordinates)
        try:
            assert(len(FEN_coordinates) == 64)
        except(AssertionError):
            print('FEN coordinates are not correct. There aren\'t 64 squares')
            sys.exit()

        for j, i in enumerate(FEN_coordinates):

            x = j % 8
            y = j // 8
            if verbose == True:
                print(f"FEN key to be assigned: {i}")
            current_piece = assign_piece(i, [x, y])
            if current_piece == None:
                s = 'blank'
            else:
                s = current_piece.get_symbol()

        #Determinar xaque mate: Legal_Moves =[while still_pieces_to_move for i in checkboard.pieces]
        # if not Legal_Moves: checkmate(current_player)


        #Getting and printing all the current pieces in board.

        pieces_symbols = [piece.get_symbol() for piece in Piece.get_alive_pieces()]
        print("Pieces on the game: ", " ".join(pieces_symbols))

        FEN_remaining = str.strip(FEN[turn_division:])

        castling_division_white = FEN_remaining.index(' ')
        FEN_turn = FEN_remaining[0]

        if FEN_turn == 'w':
            self.turn = self.white
        elif FEN_turn == 'b':
            self.turn = self.black
        else:
            raise Exception("Not a valid player in FEN")
        print(f"Game starts with {str.capitalize(a_game.turn.name)}.")

        FEN_remaining = str.strip(FEN_remaining[castling_division_white:])
        en_passant_division = FEN_remaining.index(' ')

        FEN_castling_status = FEN_remaining[:en_passant_division]
        print("Castling status in FEN:", FEN_castling_status)

        if FEN_castling_status == '-':
            pass
        else:
            for i in FEN_castling_status:
                if i =="K":
                    self.white.the_King.has_moved = False
                    self.white.the_Rook_K.has_moved = False
                elif i =="Q":
                    self.white.the_King.has_moved = False
                    self.white.the_Rook_Q.has_moved = False
                elif i =="k":
                    self.black.the_King.has_moved = False
                    self.black.the_Rook_K.has_moved = False
                elif i =="q":
                    self.black.the_King.has_moved = False
                    self.black.the_Rook_Q.has_moved = False
                else:

                    raise Exception("Not a valid character in castling status")
        print(self.game_state_to_FEN())

    def list_all_pieces(self):
        """Getting all the pieces in board"""
        x = []
        for i in range(8):
            for j in range(8):
                y = self.chessboard[i][j].get_piece()
                if y != None:
                    x.append(y)
        return x

    def print_chessboard(self):
        for y in range(8):

            rowstr = str(y_to_rank(y)) + " "

            for x in range(8):
                piece = self.chessboard[x][y].get_piece()
                char = ""
                if piece != None:
                    char = piece.get_symbol()
                else:
                    char = "□"
                rowstr += char
                rowstr += " "

            print(rowstr)
        print("  a b c d e f g h")



    def capture(self, position):
        """Eliminates piece in destination"""
        print(f"Piece to be captured is in {position}")
        self.chessboard[position[0]][position[1]].get_piece().position = [-1, -1]


    def is_legal_move(self):
        pass
    def get_relative_rank(self, y, color):
        if color == self.white:
            y = abs(y-7)
        return y

    def get_opponent(self, color):
        if color == self.white:
            return self.black
        elif color == self.black:
            return self.white

    def get_castling_string(self):
        the_string = ""
        if self.white.can_castle_K == True:
            the_string = "K"
        if self.white.can_castle_Q == True:
            the_string += "Q"
        if self.black.can_castle_K == True:
            the_string += "k"
        if self.black.can_castle_Q == True:
            the_string += "q"
        if the_string == "":
            return "-"
        return the_string
    def next_turn(self):
        if self.turn == self.white:
            self.turn = self.black
        elif self.turn == self.black:
            self.move += 1
            self.turn = self.white
    def move_attempt(self, coordinate_orig_dest):
        """Attempts to make a move. Coordinates are given in the format frfr, where 'f' is the file and 'r' is the rank, and the first two characters refer to the origin square and the last two of them to the destination square"""
        origin = coordinate_to_number(coordinate_orig_dest[:2])
        print (f"Origin coordinate: {origin}")
        destination = coordinate_to_number(coordinate_orig_dest[2:])
        #destination.append(None)
        if verbose == True:
            print (f"Destination coordinate: {destination}")
        if origin == destination:
            print("Origin and destination are the same")
            return [False]
        else: #Proceed to evaluate whether there is a piece, and whether that piece is of color of current turn.
            origin_piece = self.chessboard[origin[0]][origin[1]].get_piece()

            if origin_piece == None:
                print("there's no piece in that position")
                return [False]
            elif origin_piece.color != self.turn:
                print(f"it's {self.turn.name} to move!")
                return [False]
            else:
                #This function should evaluate if the move is pseudo-legal. It should return a list on the format of [False] or [True, special condition, special condition arguments]
                if self.is_legal_move():
                    if self.is_pseudolegal_move(origin_piece):
                        pass
                pseudo_evaluation = origin_piece.move_eval(destination)
                if pseudo_evaluation[0] == True:  #pseudo-legal move
                    special = pseudo_evaluation[1:]
                    Piece.do_move(origin_piece, destination, special)

                    return [True, origin_piece]
                else:
                    return [False]


                    #origin_piece.do_move(destination, None)




    def is_valid_piece_to_move(self, square_coord):
        piece = self.get_piece_from_coord(square_coord)
        if piece != None:
            if piece.color == self.turn:
                return True
            else:
                 return False
        else:
            return False
    def get_piece_from_coord(self, square_coord): #Just print it, for the moment
        x = file_to_x[square_coord[0]]
        print(x)
        y = rank_to_y(square_coord[1])
        print(y)
        square = self.chessboard[x][y]
        piece = square.get_piece()
        if piece != None:
            return piece
        else:
            return None

        print(result)
    def game_state_to_FEN(self):
        FEN = ""
        for j in range (8):
            blanks = 0
            for i in range(8):
                piece = self.chessboard[i][j].get_piece()


                if piece == None:
                    blanks += 1
                else:

                    if blanks != 0:

                        FEN += str(blanks)
                    letter = piece.letter
                    if piece.color == self.black:
                        letter = letter.lower()

                    FEN += letter
                    blanks = 0

            if blanks != 0:
                FEN += str(blanks)
            if j != 7:
                FEN += "/"
        FEN += " "
        #Placeholder for turn for white
        if self.turn == self.white:
            FEN += "w"
        elif self.turn == self.black:
            FEN += "b"

        FEN += " "
        #Placeholder for castling situation for both white and black, have to see if they should be separated
        FEN += self.get_castling_string()

        FEN += " "

        #Placeholder for "en passant"
        FEN += "-"

        FEN += " "

        #Placeholder for half count
        FEN += "0"

        FEN += " "
        #Placeholder for move number
        FEN += "1"
        #include turn, castling, half-move, turn number
        return FEN
    def get_piece_type_positions(self, piece_type, color, relative = True):
        positions_list = []
        for y in range(8):
            yrel = self.get_relative_rank(y, color)
            for x in range (8):

                piece = self.chessboard[x][yrel].get_piece()
                if piece != None:

                    if piece.name == piece_type and piece.color == color:
                        positions_list.append([x, y])
        return positions_list
    def get_total_value(self, color = "both"):
        alive_pieces = Piece.get_alive_pieces(color)
        value = 0
        if color == "both":
            for piece in alive_pieces:
                value += piece.value

        else:
            for piece in alive_pieces:
                if piece.color == color:
                    value += piece.value
        print(f"value is {value} for {color.name}")
        return value




a_game = Game() #Decide wether this is going to be in the module as singleton or not

if __name__ == "__main__":
    print(White)
    print(white:the_other_player())
    a_game.init_game()
    playing = True #This is going to create the loop in a While statement until the user quits
    a_game.print_chessboard()
    while playing:

        move = input("Move? (type 'q' to quit)")
        if move == 'q':
            print("Bye!")
            sys.exit()
        else:
            a_game.move_attempt(move)
            a_game.print_chessboard()

class Game():
    def is_legal():
        if is_square_pinned(self, piece):
            return False
        if is_pseudo_legal():
            if is_king_capturable() == False:
                return True
            else return [False, "King would remain in check"]
        else return [False, "Not a legal move"]

    def move_attempt():
        if is_legal() = True:
            do_move()
    def is_king_capturable():
        player = turn.the_other_player()
        destination = turn.the_king.get_square()
        for piece in player.list_of_pieces:
            if piece.move_eval(destination, special = none) == True:
                return True
        return False



    def do_move():
        pass

class Piece():
    self.color = color
    self.list_of_pieces = []
    pass

class Pawn():
    move_eval(self, dest):
        pass


#...etc

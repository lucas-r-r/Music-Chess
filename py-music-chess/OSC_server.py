"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math
import Chess
import music_engine

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client



def init_game(unused_addr, FEN):
    music_engine.white_mode.clear_mode()
    music_engine.black_mode.clear_mode()
    Chess.a_game.init_game(FEN)

    client.send_message("FEN", Chess.a_game.game_state_to_FEN())
    send_pieces_info()

def get_piece_from_coord(unused_addr, square_coord):
    piece = Chess.a_game.get_piece_from_coord(square_coord)

def is_valid_piece_to_move(unused_addr, square_coord):
    client.send_message("/game/retrieve/is_valid_piece_to_move", Chess.a_game.is_valid_piece_to_move(square_coord))

def get_pieces(unused_addr):
    print(Chess.list_all_pieces())

def send_pieces_info(unused_addr = None):
    for i in Chess.Piece.list_of_pieces:

        client.send_message("/game/piece/rel_pos", i.get_piece_info_string())

def move_attempt(unused_addr, move):

    print(f"move attempt {move} received")

    move = Chess.a_game.move_attempt(move)
    FEN = Chess.a_game.game_state_to_FEN()
    print("FEN:", FEN)

    if move[0] == True:

        send_pieces_info()
        client.send_message("/moved/piece", move[1].name)
        client.send_message("/moved/color", move[1].color.name)
        client.send_message("/moved/move_count", move[1].move_count)
        #client.send_message("/moved", str_moved_info)
        client.send_message("/turn", Chess.a_game.turn.name)
        client.send_message("/game/move", Chess.a_game.move)
        client.send_message("/FEN", FEN)
        client.send_message("/game/pieces_on_board", pieces_on_board(None, Chess.a_game.white))
        client.send_message("/game/pieces_on_board", pieces_on_board(None, Chess.a_game.black))
        value_on_board(unused_addr)

def get_check_status(unused_addr, movement):
    plus_count = movement.count('+')
    hashtag_count = movement.count('#')
    game = Chess.a_game
    #color = game.get_opponent(game.turn).name
    color = game.turn.name
    if plus_count == 1:
        check_status = "checked"
        print(f"{color} is in check!")
    elif hashtag_count == 1:
        check_status = "checkmated"
        print(f"{color} was checkmated!!!")
    else:
        check_status = "nocheck"
        print("Nobody is in check")
    client.send_message("/game/check-status", " ".join([color, check_status]))

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass


def get_piece_type_positions(unused_addr, piece_type, color):
    positions = music_engine.get_piece_type_positions(piece_type, color)
    return positions


def get_current_mode(unused_addr, color):
    if color == "white":
        mode = music_engine.white_mode.mode
    elif color == "black":
        mode = music_engine.black_mode.mode
    if len(mode) > 0:
        mode = " ".join([str(mode)])
    else:
        mode = False
    client.send_message("/mode/get/current", mode)
    #pieces = get_piece_type_positions(None, "Pawn", color)
    #mode = (music_engine.pawn_mode_generator(pieces, color))
    #print(f"Mode: {mode}")

    #client.send_message("/mode/get/from_position", mode)

def next_mode(unused_addr, color):
    print("Next mode's color:", color)
    if color == "white":
        color_obj = Chess.a_game.white
    elif color == "black":
        color_obj = Chess.a_game.black
    pawn_positions = Chess.a_game.get_piece_type_positions("Pawn", color_obj)
    print("Pawn positions:", pawn_positions)
    next_mode = music_engine.pawn_mode_generator(pawn_positions, color)
    if color == "white":
        music_engine.white_mode.receive_next_mode(next_mode)
    elif color == "black":
        music_engine.black_mode.receive_next_mode(next_mode)

    else:
        print("No valid player color given")
    print(f"Next mode for {color}, {next_mode}")

def pawn_advance(unused_addr, color):

    if color == "white":
        color_obj = Chess.a_game.white
    elif color == "black":
        color_obj = Chess.a_game.black
    pawn_positions = Chess.a_game.get_piece_type_positions("Pawn", color_obj)
    print("Pawn positions:", pawn_positions)
    advance_value = music_engine.pawn_advance(pawn_positions, color)
    message = " ".join([color, str(advance_value)])
    client.send_message("/game/pawn_advance", message)

def add_note(unused_addr, color):
#    try:
        if color == "white":

            note = music_engine.white_mode.add_note()
        elif color == "black":
            note = music_engine.black_mode.add_note()
        if note != False:
            print(f"Note to play: {note} for {color}")
            #message = " ".join([color, str(note)])
            #print(message)
            client.send_message("/mode/noteon", [color, note])
#    except TypeError as e:
#        print("No more notes to play in next mode!")



def remove_note(unused_addr, color):
    if color == "white":

        note = music_engine.white_mode.remove_note()
    elif color == "black":
        note = music_engine.black_mode.remove_note()
    if note != False:
        print("Note to remove:", {note})
        #message = " ".join([color, str(note)])
        #print(message)
        client.send_message("/mode/noteoff", [color, note])

def pieces_on_board(unused_addr, color = "both"):
    message = str(len(Chess.Piece.get_alive_pieces(color)))
    try:
        color = color.name
    except TypeError as e:
        pass
    message = " ".join([color, message])
    print(message)

    return message

def value_on_board(unused_addr, color = "both"):
    #in this implementation, color parameter is ignored and it sends both values
    value = Chess.a_game.get_total_value(Chess.a_game.white)
    message = " ".join([Chess.a_game.white.name, str(value)])
    client.send_message("/game/total_value", message)
    value = Chess.a_game.get_total_value(Chess.a_game.black)
    message = " ".join([Chess.a_game.black.name, str(value)])
    client.send_message("/game/total_value", message)

def promotion_choice(unused_addr, piece):
    Chess.a_game.promotion_choice = piece




def test_code(unused_addr, test_args, t2, t3):
     print("Hello world")
     print(test_args)
     print(t2)
     print(t3)
     print("unused address is:", unused_addr)

if __name__ == "__main__":
    client = udp_client.SimpleUDPClient("127.0.0.1", 12345)
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/filter", print)
    dispatcher.map("/volume", print_volume_handler, "Volume")
    dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)
    dispatcher.map("/init_game", init_game)
    dispatcher.map("/get_all_pieces", get_pieces)
    dispatcher.map("/move", move_attempt)
    dispatcher.map("/game/is_valid_piece_to_move", is_valid_piece_to_move)
    dispatcher.map("/test", test_code)
    dispatcher.map("/get_piece_type_positions", get_piece_type_positions)
    dispatcher.map("/get/game/pawn_advance", pawn_advance)
    dispatcher.map("/mode/get/current", get_current_mode)
    dispatcher.map("/mode/next", next_mode)
    dispatcher.map("/mode/add_note", add_note)
    dispatcher.map("/mode/remove_note", remove_note)
    dispatcher.map("/game/get_pieces_on_board", pieces_on_board)
    dispatcher.map("/game/get_value_on_board", value_on_board)
    dispatcher.map("/get/check-status-from-algebraic", get_check_status)
    dispatcher.map("/game/promotion_choice", promotion_choice)
    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))


    server.serve_forever()

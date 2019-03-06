
############################################################################
# FILE: four_in_a_row.py
# WRIETER: guy gueta, guy245, 203428222
# EXERCISE: 12
# DESCRIPTION: a file contains the main program that runs the 4_in_a_row
# game
########################################################################

import tkinter as T
import graphics
import sys
IS_HUMAN_INDEX = 1
SERVER_ARGS = 2
CLIENT_ARGS = 3
MIN_PORT = 1000
MAX_PORT = 65535
PORT_INDEX = 2
IP_INDEX = 3
ERROR_MSG = "illegal program argument was inserted "
CLIENT = "client"
SERVER = "server"
HUMAN_PLAYER = "human"
AI_PLAYER = "ai"

def run_game():
    """ runs a single player in a four_in_a_row game , we can choose if the
    player gonna be us to play or the computer ,if we inserted the params
    in a wrong way the func' gonna print an error msg and return none  """
    if len(sys.argv) != SERVER_ARGS + 1 and len(sys.argv) != CLIENT_ARGS +1\
            or not MIN_PORT <= int(sys.argv[PORT_INDEX]) <= MAX_PORT or \
             sys.argv[IS_HUMAN_INDEX] != HUMAN_PLAYER and \
                                      sys.argv[IS_HUMAN_INDEX] != AI_PLAYER :
         print(ERROR_MSG)
         return None
    parent = T.Tk()
    port = int(sys.argv[PORT_INDEX])
    if len(sys.argv) == CLIENT_ARGS + 1:
        ip = sys.argv[IP_INDEX]
        graphics.Graphics(parent,port, sys.argv[IS_HUMAN_INDEX], ip)
        parent.title(CLIENT)
    else:
        graphics.Graphics(parent,port,sys.argv[IS_HUMAN_INDEX])
        parent.title(SERVER)
    parent.mainloop()


if __name__ == '__main__':
    run_game()

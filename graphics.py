# FILE graphics.py
# WRIETER: guy gueta, guy245, 203428222
# EXERECISE: ex12
# DESCRIPTION: contains the class graphics which is responsible for the
# graphic interface of the game and the communication between the players

import tkinter as tki
from game import Game
from communicator import Communicator
import socket
from ai import AI


class Graphics:
    """class that operate the graphic interface and communication of
    four_in_a_row game"""
    FIRST_COLUMN = 0
    TEXT1 = 'Player 1 turn'
    TEXT2 = 'Player 2 turn'
    TEXT3 = 'use LEFT/RIGHT keys to choose a column'
    TEXT4 = 'use DOWN key to drop a disc'
    TEXT5 = 'ILLEGAL MOVE'
    FIRST_TURN = 0
    MESSAGE_DISPLAY_TIMEOUT = 1000
    MAIN_WINDOW_WIDTHE = 350
    SQUARE_SIZE = 50
    TOP_FRAME_HEIGHT = 100
    MIDDLE_FRAME_HEIGHT = 300
    OVAL_1 = 5
    OVAL_2 = 45
    BLUE1 = 'dodger blue'
    FILL_WHITE = "white"
    TAG_OVAL = "oval"
    CANVAS_WIDTH = 370
    FILL_RED = "red"
    W_ANCHOR = "w"
    NW_ANCHOR = "nw"
    TAG_PLAYER = "player"
    BD10 = 10
    CANVAS5 = 5
    CANVAS_0 = 0
    FONT16 = 16
    FONT12 = 12
    CANVAS40 = 40
    CANVAS70 = 70
    SW_ANCHOR = "sw"
    CANVAS185 = 185
    CANVAS45 = 45
    FILL_GOLD = "gold"
    CANVAS85 = 85
    ILLEGAL_MSG = "illegal_msg"
    FONT18 = 18
    CANVAS25 = 25
    MIN_MOVE = 0
    MAX_MOVE = 6
    TAG_ARROW = "arrow"
    CHANGE_ARROW = 54
    FILL_GREEN = 'lawn green'
    TAG_HUMAN = 'human'
    TAG_AI = "ai"
    MOVE_RIGHT = "<Right>"
    MOVE_LEFT = "<Left>"
    MOVE_DOWN = '<Down>'
    CHANGE = 1

    def __init__(self, parent, port, player, ip=None, player_turn=True):
        """initiate a graphics object
        :param parent: a tkinter root(main window)
        :param port: the port the player choose that manage the
        communication
        :param player: type of player- human or ai
        :param ip: an ip required if the player defines as the client
        :param player_turn: defines if its the player turn to play- changes
        through the game"""
        self.__player = player
        self.__player_turn = player_turn
        if ip:
            self.__player_turn = False  # in order the server to get the
            # first turn
        self.__parent = parent
        self.__communicator = Communicator(self.__parent, port, ip)  # to
        # unblock the communication
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_messege)
        self.__game_board = Game()  # initiate a game object
        # now dividing the main window to three frames- top for title and
        # announcements, middle for the board an bottom for rules and state
        self.__top_frame = tki.Frame(self.__parent,
                                     width=self.MAIN_WINDOW_WIDTHE,
                                     height=self.TOP_FRAME_HEIGHT,
                                     bd=10, relief=tki.GROOVE)
        self.__top_frame.pack(side=tki.TOP)
        self.__middle_frame = tki.Frame(self.__parent,
                                        width=self.MAIN_WINDOW_WIDTHE,
                                        height=self.MIDDLE_FRAME_HEIGHT,
                                        bd=self.BD10, relief=tki.GROOVE)
        self.__middle_frame.pack()
        self.__bottom_frame = tki.Frame(self.__parent,
                                        width=self.MAIN_WINDOW_WIDTHE,
                                        height=self.TOP_FRAME_HEIGHT,
                                        bd=self.BD10,
                                        relief=tki.GROOVE)
        self.__bottom_frame.pack(side=tki.BOTTOM)
        self.create_widgets()
        self.create_ovals(self.__middle_frame)
        self.moves()
        self.__arrow_point = self.FIRST_COLUMN  # initiate arrow at first
        # column

    def create_ovals(self, frame):
        """initiate canvases represnt the discs container"""
        for i in range(self.__game_board.LENTGH):
            for j in range(self.__game_board.WIDTH):
                square = tki.Canvas(frame, width=self.SQUARE_SIZE,
                                    height=self.SQUARE_SIZE,
                                    bg=self.BLUE1)
                square.create_oval(self.OVAL_1, self.OVAL_1, self.OVAL_2,
                                   self.OVAL_2,
                                   fill=self.FILL_WHITE, tag=self.TAG_OVAL)
                square.grid(row=i, column=j)

    def create_widgets(self):
        """creates and pack all main canvases texts and images that make up
        the design"""
        self.__top_canvas = tki.Canvas(self.__top_frame,
                                       width=self.CANVAS_WIDTH,
                                       height=self.TOP_FRAME_HEIGHT,
                                       bg=self.FILL_WHITE)
        self.__top_canvas.pack()
        self.__bottom_canvas = tki.Canvas(self.__bottom_frame,
                                          width=self.CANVAS_WIDTH,
                                          height=self.TOP_FRAME_HEIGHT,
                                          bg=self.FILL_WHITE)
        self.__bottom_canvas.pack()
        self.__bottom_canvas.create_text(self.CANVAS5, self.CANVAS_0,
                                         anchor=self.NW_ANCHOR,
                                         text=self.TEXT1,
                                         fill=self.FILL_RED,
                                         tag=self.TAG_PLAYER,
                                         font=(False, self.FONT16))
        self.__bottom_canvas.create_text(self.CANVAS5, self.CANVAS40,
                                         anchor=self.W_ANCHOR,
                                         text=self.TEXT3,
                                         fill=self.BLUE1,
                                         font=(False, self.FONT12))
        self.__bottom_canvas.create_text(self.CANVAS5, self.CANVAS70,
                                         anchor=self.SW_ANCHOR,
                                         text=self.TEXT4,
                                         fill=self.BLUE1,
                                         font=(False, self.FONT12))
        self.__title_file = tki.PhotoImage(file='title.gif')
        self.__top_canvas.create_image(self.CANVAS185, self.CANVAS40,
                                       image=self.__title_file)
        self.__arrow = tki.PhotoImage(file="giphy.gif")
        self.__win_file = tki.PhotoImage(file='youwin.png')
        self.__lose_file = tki.PhotoImage(file='lose.png')
        self.__draw_file = tki.PhotoImage(file='draw.png')
        self.__top_canvas.focus_set()  # focusing key_board to top canvas

    def check_for_winner(self):
        """using the game_board function of checking winner and show the
        winning state on the screen"""
        if self.__game_board.get_winner() == \
                self.__game_board.get_other_player():  # after making a move
            #  the turn changes so other player means winning
            self.mark_sequence()  # marking the winning discs
            self.__top_canvas.create_image(self.CANVAS185, self.CANVAS45,
                                           image=self.__win_file)
            self.__player_turn = False  # allowing no more turns
        elif self.__game_board.get_winner() == \
                self.__game_board.get_current_player():
            self.mark_sequence()
            self.__top_canvas.create_image(self.CANVAS185, self.CANVAS45,
                                           image=self.__lose_file)
            self.__player_turn = False
        elif self.__game_board.get_winner() == self.__game_board.DRAW:
            self.__top_canvas.create_image(self.CANVAS185, self.CANVAS45,
                                           image=self.__draw_file)
            self.__player_turn = False

    def callback(self, event):
        """the function bind to the event of pressing the down key in order
        to drop a disc. it updates the move on the game board and update the
        screen in accordance"""
        if self.__player_turn:  # allows the play only in turn
            try:
                self.__game_board.make_move(self.__arrow_point)  # making
                # the move according to the place of the arrow
                x, y = self.__game_board.get_last_disc()
                message = str(self.__arrow_point)
                # sending the message after making a move in order the
                # other player's board to update
                self.__communicator.send_message(message)
                # update the place in the  board chosen to the appropriate
                # color
                if self.__game_board.get_current_player():
                    self.__middle_frame.grid_slaves(row=x, column=y)[
                        0].itemconfig(self.TAG_OVAL, fill=self.FILL_RED)
                else:
                    self.__middle_frame.grid_slaves(row=x, column=y)[
                        0].itemconfig(self.TAG_OVAL, fill=self.FILL_GOLD)
                # now we update the indication of player_turn
                if not self.__game_board.get_winner():
                    if self.__game_board.get_current_player():
                        self.__bottom_canvas.itemconfig(self.TAG_PLAYER,
                                                        text=self.TEXT2,
                                                        fill=self.FILL_GOLD)
                    else:
                        self.__bottom_canvas.itemconfig(self.TAG_PLAYER,
                                                        text=self.TEXT1,
                                                        fill=self.FILL_GOLD)
                self.check_for_winner()
                self.__player_turn = False  # changing the turn
            except Exception:  # display a message for an instance when a
                # wrong column was chosen
                self.__bottom_canvas.create_text(self.CANVAS185,
                                                 self.CANVAS85,
                                                 text=self.TEXT5,
                                                 fill=self.FILL_RED,
                                                 tag=self.ILLEGAL_MSG,
                                                 font=(False, self.FONT18))
                self.__bottom_canvas.after(self.MESSAGE_DISPLAY_TIMEOUT,
                                        lambda: self.__bottom_canvas.delete(
                                               self.ILLEGAL_MSG))

    def ai_move(self, ai):
        """makes a move and update the screen automatically using the ai
        object gives as parameter"""
        if self.__player_turn:
            # the move is set according to the find_legal_move_func'
            ai.find_legal_move(self.__game_board, self.__game_board.make_move)
            # same as callback apart from the exception which handled in
            # 'find_legal_move'
            x, y = self.__game_board.get_last_disc()
            message = str(y)
            self.__communicator.send_message(message)
            if self.__game_board.get_current_player():
                self.__middle_frame.grid_slaves(row=x, column=y)[
                    0].itemconfig(
                    self.TAG_OVAL,
                    fill=self.FILL_RED)
            else:
                self.__middle_frame.grid_slaves(row=x, column=y)[
                    0].itemconfig(
                    self.TAG_OVAL,
                    fill=self.FILL_GOLD)
            if not self.__game_board.get_winner():
                if self.__game_board.get_current_player():
                    self.__bottom_canvas.itemconfig(self.TAG_PLAYER,
                                                    text=self.TEXT2,
                                                    fill=self.FILL_GOLD)
                else:
                    self.__bottom_canvas.itemconfig(self.TAG_PLAYER,
                                                    text=self.TEXT1,
                                                    fill=self.FILL_RED)
            self.check_for_winner()
            self.__player_turn = False

    def moves(self):
        """distinguish between a human and ai player and allows the moves
        accordingly. called in the init function"""
        if self.__player == self.TAG_HUMAN:
            self.create_arrow()
        else:
            ai = AI()  # creating the ai object for this running
            self.ai_move(ai)

    def create_arrow(self):
        """in charge of all the bindings while the player is human"""
        self.__top_canvas.create_image(self.CANVAS25, self.CANVAS85,
                                       image=self.__arrow,
                                       tag=self.TAG_ARROW)
        # creating the arrow first
        self.__top_canvas.bind(self.MOVE_RIGHT, self.move_arrow_right)
        self.__top_canvas.bind(self.MOVE_LEFT, self.move_arrow_left)
        self.__top_canvas.bind(self.MOVE_DOWN, self.callback)
        self.__top_canvas.register(self.__arrow)

    def move_arrow_right(self, event):
        """moves arrow to the right while pressing RIGHT"""
        if self.MIN_MOVE <= self.__arrow_point < self.MAX_MOVE:
            self.__arrow_point += self.CHANGE  # updates arrow location
            event.widget.move(self.TAG_ARROW, self.CHANGE_ARROW,
                              self.CANVAS_0)

    def move_arrow_left(self, event):
        """moves arrow to the left while pressing LEFT"""
        if self.MIN_MOVE < self.__arrow_point <= self.MAX_MOVE:
            self.__arrow_point -= self.CHANGE
            event.widget.move(self.TAG_ARROW, -self.CHANGE_ARROW,
                              self.CANVAS_0)

    def mark_sequence(self):
        """using the winning_sec_lst variable of the game_board and marks
        the winning strait"""
        for coor in self.__game_board.get_winning_sec_lst():
            self.__middle_frame.grid_slaves(row=coor[0], column=coor[1])[
                0].config(bg=self.FILL_GREEN)

    def __handle_messege(self, text):
        """when receiving a message updates the game_board and screen in
        accordance and makes all the checks for winner like in callback"""
        if text:
            arrow_point = int(text)
            self.__game_board.make_move(arrow_point)
            x, y = self.__game_board.get_last_disc()
            if self.__game_board.get_current_player():
                self.__middle_frame.grid_slaves(row=x, column=y)[
                    0].itemconfig(self.TAG_OVAL, fill=self.FILL_RED)
            else:
                self.__middle_frame.grid_slaves(row=x, column=y)[
                    0].itemconfig(self.TAG_OVAL, fill=self.FILL_GOLD)
            if not self.__game_board.get_winner():
                if self.__game_board.get_current_player():
                    self.__bottom_canvas.itemconfig(self.TAG_PLAYER,
                                                    text=self.TEXT2,
                                                    fill=self.FILL_GOLD)
                else:
                    self.__bottom_canvas.itemconfig(self.TAG_PLAYER,
                                                    text=self.TEXT1,
                                                    fill=self.FILL_RED)
            # changing the terms of win and lose-opposite than callback
            if self.__game_board.get_winner() == \
                                      self.__game_board.get_current_player():
                self.mark_sequence()
                self.__top_canvas.create_image(self.CANVAS185, self.CANVAS45,
                                               image=self.__win_file)
                self.__player_turn = False
                return  # in order to freeze the game for the second player
            elif self.__game_board.get_winner() == \
                                        self.__game_board.get_other_player():
                self.mark_sequence()
                self.__top_canvas.create_image(self.CANVAS185, self.CANVAS45,
                                               image=self.__lose_file)
                self.__player_turn = False
                return
            elif self.__game_board.get_winner() == self.__game_board.DRAW:
                self.__top_canvas.create_image(self.CANVAS185, self.CANVAS45,
                                               image=self.__draw_file)
                self.__player_turn = False
                return
            self.__player_turn = True
            if self.__player == self.TAG_AI:  # in case its an ai the message
                # activates the moves func again
                self.moves()


print(socket.gethostbyname(socket.gethostname()))


############################################################################
# FILE: game.py
# WRIETER: guy gueta, guy245, 203428222
# EXERCISE: 12
# DESCRIPTION: a file contains the Class game
########################################################################


class Game:
    """ a Class that represents the all duration of the game in paton data
    base , during all the we allays updates class ddependson the
    situation """

    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    LENTGH = 6
    WIDTH = 7
    FIRST_TURN = 0
    EMPTY_SQUARE = '_'
    WIN_NUM = 4
    FULL_BOARD = 42
    NO_DISC = None
    WIN_LIST = []
    MODULO = 2
    CHANGE = 1
    DEFAULT_VAL = 0
    START = -3
    END = 4

    def __init__(self):
        """ init our game class"""
        self.__board = [[self.EMPTY_SQUARE] * self.WIDTH for i in
                                                           range(self.LENTGH)]
        self.__turn = self.FIRST_TURN
        self.__last_disc = self.NO_DISC
        self.__winning_sec_lst = self.WIN_LIST

    def make_move(self, column):
        """

        :param column: the value of the column coordination that we want to
        insert the  disc
        :return: the func returns none and updates self.__board ,
        self.__last_disc and self.__turn with value depends on the turn
        """
        row = self.check_board(column) # we use check_board to get the row
        # cords
        if self.__turn % self.MODULO == self.PLAYER_ONE:
            self.__board[row][column] = self.PLAYER_ONE
            self.__last_disc = row, column
            self.__turn += self.CHANGE
        else:
            self.__board[row][column] = self.PLAYER_TWO
            self.__last_disc = row, column
            self.__turn += self.CHANGE

    def check_board(self, column):
        """

        :param column: the value of the column coordination that we want to
        insert the  disc
        :return: the value of the row coordination in the board
        """
        if self.__board[0][column] != self.EMPTY_SQUARE:
            raise Exception("illegal move")
        counter = self.LENTGH - self.CHANGE
        while self.__board[counter][column] != self.EMPTY_SQUARE:
            counter -= self.CHANGE
        return counter

    def get_winner(self):
        """
        the func checks at each stage of the game if the player who insert
        the last disc won
        :return: the player if the player who insert disc won , draw if the
         board is full or None if none of them happened
        """
        x, y = self.__last_disc
        player = self.get_player_at(x, y)
        if self.check_horizontal(x, y, player) or self.check_vertical(x, y,
            player) or self.check_slant_1(x, y, player) or \
                self.check_slant_2(x, y, player):
            return player
        else:
            if self.__turn == self.FULL_BOARD:
                return self.DRAW
            else:
                return None

    def check_horizontal(self, row, col, player):
        """
        the func checks if the player who insert the last disk made made a
        line of 4 in the horizontal direction
        :param row: the row cords on the board of the disc that been inserted
        :param col: the col cords on the board of the disc that been inserted
        :param player: the player who insert the last disc
        :return: true if the player made for in a line False else
        """
        counter = self.DEFAULT_VAL
        temp_list = []
        for i in range(self.START, self.END):
            if self.is_valid(row, col + i):
                if self.__board[row][col + i] == player:
                    counter += self.CHANGE
                    temp_list.append((row, col + i))
                    if counter == self.WIN_NUM:
                        self.__winning_sec_lst = temp_list
                        return True
                else:
                    counter = self.DEFAULT_VAL
                    temp_list = []
        else:
            return False

    def check_vertical(self, row, col, player):
        """
        the func checks if the player who insert the last disk made made a
        line of 4 in the vertical direction
        :param row: the row cords on the board of the disc that been inserted
        :param col: the col cords on the board of the disc that been inserted
        :param player: the player who insert the last disc
        :return: true if the player made for in a line False else """
        counter = self.DEFAULT_VAL
        temp_list = []
        for i in range(self.START,self.END):
            if self.is_valid(row + i, col):
                if self.__board[row + i][col] == player:
                    counter += self.CHANGE
                    temp_list.append((row + i, col))
                    if counter == self.WIN_NUM:
                        self.__winning_sec_lst = temp_list
                        return True
                else:
                    counter = self.DEFAULT_VAL
                    temp_list = []
        else:
            return False

    def check_slant_1(self, row, col, player):
        """the func checks if the player who insert the last disk made made a
        line of 4 in the in up to down slant direction
        :param row: the row cords on the board of the disc that been inserted
        :param col: the col cords on the board of the disc that been inserted
        :param player: the player who insert the last disc
        :return: true if the player made for in a line False else"""
        counter = self.DEFAULT_VAL
        temp_list = []
        for i in range(self.START, self.END):
            if self.is_valid(row + i, col + i):
                if self.__board[row + i][col + i] == player:
                    counter += self.CHANGE
                    temp_list.append((row + i, col + i))
                    if counter == self.WIN_NUM:
                        self.__winning_sec_lst = temp_list
                        return True
                else:
                    counter = self.DEFAULT_VAL
                    temp_list = []
        else:
            return False

    def check_slant_2(self, row, col, player):
        """ the func checks if the player who insert the last disk made made a
        line of 4 in the in down to up slant direction
        :param row: the row cords on the board of the disc that been inserted
        :param col: the col cords on the board of the disc that been inserted
        :param player: the player who insert the last disc
        :return: true if the player made for in a line False else"""
        counter = self.DEFAULT_VAL
        temp_list = []
        for i in range(self.START, self.END):
            if self.is_valid(row - i, col + i):
                if self.__board[row - i][col + i] == player:
                    counter += self.CHANGE
                    temp_list.append((row - i, col + i))
                    if counter == self.WIN_NUM:
                        self.__winning_sec_lst = temp_list
                        return True
                else:
                    counter = self.DEFAULT_VAL
                    temp_list = []
        else:
            return False

    def is_valid(self, row, col):
        """
        this is a help func to the 4 funcs that came before here that checks
        if we made 4 in a line , the func checks if the the cords that we
        insert are not out of the board index
        :param row: the value of the row in the cord that we check
        :param col: the value of the col in the cord that we check
        :return: true if the cord that we inserted are in the index False
        else
        """
        if row < self.DEFAULT_VAL or row >= self.LENTGH or col < \
                                     self.DEFAULT_VAL or col  >= self.WIDTH:
            return False
        return True

    def get_player_at(self, row, col):
        """
        the func help us to check in a certain cord on the board which
        player disc in it  or if its empty
        :param row: the value of the row in the cord that we check
        :param col: the value of the col in the cord that we check
        :return: the certain player that insert the disc we checked or None
        if its an empty place on the board
        """
        if self.__board[row][col] == self.PLAYER_ONE:
            return self.PLAYER_ONE
        elif self.__board[row][col] == self.PLAYER_TWO:
            return self.PLAYER_TWO
        else:
            return None

    def get_current_player(self):
        """
        :return: the current player that this is his turn
        """
        if self.__turn % self.MODULO == self.PLAYER_ONE:
            return self.PLAYER_ONE
        else:
            return self.PLAYER_TWO

    def get_other_player(self):
        """

        :return: the func checks who is the current_player and by thet
        returns the other one
        """
        if self.get_current_player():
            return self.PLAYER_ONE
        else:
            return self.PLAYER_TWO

    def get_board(self):
        """

        :return: self.__board
        """
        return self.__board

    def get_turn(self):
        """

        :return: self__turn
        """
        return self.__turn

    def get_last_disc(self):
        """

        :return: self.__last_disc
        """
        return self.__last_disc

    def get_winning_sec_lst(self):
        """

        :return: elf.__winning_sec_lst
        """
        return self.__winning_sec_lst


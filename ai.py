from game import Game
import random

############################################################################
# FILE: ai.py
# WRIETER: guy gueta, guy245, 203428222
# EXERCISE: 12
# DESCRIPTION: a file that contains the Class AI
########################################################################


class AI:
    """ a class that represents the moves that been done by the computer in
    a game of 4 in a row  """
    COLUMN_NUM = 7
    ERROR_MSG = 'No possible AI moves'

    def find_legal_move(self, g, func, timeout=None):
        """ the func is looking for a legal move to lay by the computer on
        the board and if its found one , it updates it on the board game
        and returns none if she found one , if not it raise a msg as
        exception
        :param g : an object from class game , that is the game board that
        we updates the moves on it in payton data base
        :param func: the func that checks the legality of the move and
        updates him on the board game , the func belongs to class game
        :param timeout: irrelevant
        """
        num_lst = [i for i in range(self.COLUMN_NUM)]
        random.shuffle(num_lst)
        for col in num_lst:
            try:
                func(col)
                return
            except Exception:
                continue
        else:
            raise Exception(self.ERROR_MSG)

###########################################################################
# FILE : game.py
# WRITER : Lior Paz, lioraryepaz, 206240996
# | Eran Gilead, eran.gilead, 203344130
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION : Contains Game Class - follow the logic of four in a row game
###########################################################################

from math import fabs
# we use it for switching the player


class Game:
    """
    Creates a Four-in-a-Row game with 2 players, you could play until
    reaching a winner or a draw
    """
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    MOVES = [(1, 0), (0, -1), (1, -1), (-1, -1)]
    FIRST_ROW = 0
    BOARD_ROW = 6
    BOARD_COLUMN = 7
    EXCEPTION = 'Illegal move'

    def __init__(self):
        """
        Constructor
        """
        self.__game_board = [[None] * Game.BOARD_COLUMN for _ in range(
            Game.BOARD_ROW)]
        self.__column_track_dict = {column: 0 for column in range(
            1, Game.BOARD_COLUMN + 1)}
        # dict with number of discs in every column, keys range are 1-7
        self.__current_player = 0
        # the player who supposed to play next
        self.__last_disc = (0, 0)
        self.__who_am_i = None
        # which player this game belongs to

    def __create_game_board(self):
        """
        private Game method
        :return: list of lists
        """
        board = [[None] * Game.BOARD_COLUMN for _ in range(Game.BOARD_ROW)]
        return board

    def get_who_am_i(self):
        """
        Game method
        :return: Player ONE or Player TWO
        """
        return self.__who_am_i

    def set_current_player(self):
        """
        Game method
        switch between player ONE and Player TWO
        :return:  None
        """
        player = fabs(self.__current_player - 1)
        if player:
            self.__current_player = Game.PLAYER_TWO
        else:
            self.__current_player = Game.PLAYER_ONE

    def __set_last_disc(self, coordinate):
        """
        change last disc added to the board
        :param coordinate: tuple (row, col)
        :return: None
        """
        self.__last_disc = coordinate

    def __set_column_track_dict(self, column_num):
        """
        add discs to column_track_dict
        :param column_num: integer 1-7
        :return: None
        """
        self.__column_track_dict[column_num] += 1

    def get_column_track_dict(self):
        """
        Game method
        :return:  column_track_dict dict
        """
        return self.__column_track_dict

    def make_move(self, column_num):
        """
        the central make_move function of the game
        :param column_num: column that a disc was inserted to, integer
        between 0-6
        :return: None
        """
        column_num += 1
        # column adjustment between 0-6 to 1-7
        if not column_num > Game.BOARD_COLUMN:
            # range check
            if not self.get_winner():
                # winner check
                row_num = Game.BOARD_ROW - self.__column_track_dict[column_num]
                if not row_num < 1:
                    # full column check
                    self.__game_board[row_num - 1][
                        column_num - 1] = self.__current_player
                    # disc assignment
                    self.__set_last_disc((row_num - 1, column_num - 1))
                    # last disc update
                    self.__set_column_track_dict(column_num)
                    # column_track_dict update
                    return
        raise Exception(Game.EXCEPTION)

    def get_winner(self):
        """
        Game method
        :return: Integer 0-2 for player one, player 2 & draw or None for no
        winning status
        """
        won_lst = self.check_status(self.__last_disc)
        # the list of won discs
        if won_lst:
            return self.get_current_player()
        if None not in self.__game_board[Game.FIRST_ROW]:
            return Game.DRAW
        return None

    def check_status(self, last_disc, win_factor=3):
        """
        check for a winning disc sequence
        :param last_disc: self.last_disc tuple(x,y)
        :param win_factor: 3 for normal win - default, 2 for ai block check,
        1 for ai
        self_win check
        :return: won list if there is any, False otherwise
        """
        player = self.get_current_player()
        for i, j in Game.MOVES:
            # possible winning directions
            x, y = last_disc[0], last_disc[1]
            while (-1 < x < Game.BOARD_ROW and y > -1) and \
                            self.__game_board[x][y] == player:
                # search for the first disc in a sequence
                x, y = x + i, y + j
            x, y = x - i, y - j
            # return to the first disc in the sequence
            counter_lst = []
            while (y < Game.BOARD_COLUMN and -1 < x < Game.BOARD_ROW) and \
                            self.__game_board[x][y] == player:
                counter_lst.append((x, y))
                x, y = x - i, y - j
                # count the winning strike
            if len(counter_lst) > win_factor:
                return counter_lst
        return False

    def get_player_at(self, row, col):
        """
        Game method
        :param row: integer 0-5
        :param col: integer 0-6
        :return: 0-1 for Player ONE & Player TWO or None
        """
        return self.__game_board[row][col]

    def get_last_disc(self):
        """
        Game method
        :return: tuple
        """
        return self.__last_disc

    def get_current_player(self):
        """
        Game method
        :return: 0-1 Player ONE or Player TWO
        """
        return self.__current_player

    def get_board(self):
        """
        Game method
        :return: list of lists
        """
        return self.__game_board

    def set_player(self, player):
        """
        Game method
        :param player: 0-1 Player ONE or Player TWO
        :return: None
        """
        self.__who_am_i = player

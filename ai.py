###########################################################################
# FILE : ai.py
# WRITER : Lior Paz, lioraryepaz, 206240996
# | Eran Gilead, eran.gilead, 203344130
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION : Contains AI Class - let the computer play with smart moves
###########################################################################

from random import choice


class AI:
    EXCEPTION = "No possible AI moves."
    # Position constants
    DIAGONAL_UP = 2
    DIAGONAL_DOWN = -2
    LINE = 1
    COLUMN = -1
    # when to stop part of AI recursion
    COUNTER_TIMEOUT = 10

    def __init__(self):
        """
        Constructor
        """
        self.__my_last_play = (0, 0)

    def find_legal_move(self, g, func, timeout=None):
        """
        suggest the best legal move to perform next
        :param g: Game object
        :param func: func to perform the next move
        :param timeout: Default - None, when to stop the recursion
        :return: None
        """
        column_status = g.get_column_track_dict()
        # dict contains columns and number of discs in each column
        optional_columns = self.get_optional_columns(g, column_status)
        # which columns not full
        g.set_current_player()
        discs_in_a_row = g.check_status(g.get_last_disc(), 1)
        # gives a sequence of the opponent player discs - 2 and above
        g.set_current_player()
        if discs_in_a_row:
            if self.block(discs_in_a_row, optional_columns, func, g,
                          column_status):
                # try and block the opponent
                return
        discs_in_a_row = g.check_status(self.__my_last_play, 0)
        # gives a sequence of the player discs - 1 and above
        if discs_in_a_row:
            if self.block(discs_in_a_row, optional_columns, func, g,
                          column_status):
                # try and complete the player discs towards victory
                return
        if not optional_columns:
            raise Exception(AI.EXCEPTION)
        # random move is there is no 'smart' move to perform
        choose_button = func(choice(optional_columns))
        # perform the func
        choose_button('click')

    def block(self, discs_in_a_row, optional_columns, func, g, column_status,
              counter=0):
        """
        search where to locate the next disc
        :param discs_in_a_row: sequence of discs
        :param optional_columns: available columns
        :param func: func to perform move
        :param g: Game object
        :param column_status:  dict contains columns and number of discs in
        each column
        :param counter: track number of recursion perform, an integer
        :return: True or None
        """
        position = self.get_position(discs_in_a_row)
        # what position the sequence is - row, line, diagonal. random for
        # one disc
        if position == AI.COLUMN:
            column = discs_in_a_row[0][1] + 1
            # the requested column for the move
            if column in optional_columns:
                choose_button = func(column)
                # perform the func
                choose_button('click')
                return True
        elif position == AI.LINE:
            right_end = (discs_in_a_row[-1][0], discs_in_a_row[-1][1] + 1)
            left_end = (discs_in_a_row[0][0], discs_in_a_row[0][1] - 1)
            # the coordinates of the requested spots
            if self.operate_move(g, right_end, left_end, column_status, func):
                # check if the spot is available - is it free, and if there is
                # a disc under it (to 'catch' it)
                return True
        elif position == AI.DIAGONAL_UP:
            right_end = (discs_in_a_row[-1][0] - 1, discs_in_a_row[-1][1] + 1)
            left_end = (discs_in_a_row[0][0] + 1, discs_in_a_row[0][1] - 1)
            if self.operate_move(g, right_end, left_end, column_status, func):
                return True
        elif position == AI.DIAGONAL_DOWN:
            right_end = (discs_in_a_row[-1][0] - 1, discs_in_a_row[-1][1] + 1)
            left_end = (discs_in_a_row[0][0] + 1, discs_in_a_row[0][1] - 1)
            if self.operate_move(g, right_end, left_end, column_status, func):
                return True
        if counter > AI.COUNTER_TIMEOUT:
            # base case
            return
        counter += 1
        # we call the func in recursion so when we have only one disc,
        # to try all of the options to try and win before
        # 'giving up' and return None
        return self.block(discs_in_a_row, optional_columns, func, g,
                          column_status, counter)

    def get_optional_columns(self, g, column_status):
        """
        calculate available columns
        :param g: Game object
        :param column_status:  dict contains columns and number of discs in
        each column
        :return: list of optional columns
        """
        columns = list(column_status)
        # turns dict to list
        optional_columns = []
        for column in columns:
            if column_status[column] < g.BOARD_ROW:
                optional_columns.append(column)
        return optional_columns

    def get_position(self, coordinates):
        """
        get the position of a sequence - line, row, up diagonal or down
        diagonal
        :param coordinates: list of tuples
        :return: integer represents position state
        """
        if len(coordinates) > 1:
            # determining the position using index arithmetic
            column = coordinates[0][1] - coordinates[1][1]
            row = coordinates[0][0] - coordinates[1][0]
            if column == 0:
                return AI.COLUMN
            elif row == 0:
                return AI.LINE
            else:
                if row > 0:
                    return AI.DIAGONAL_UP
                if row < 0:
                    return AI.DIAGONAL_DOWN
        else:
            # random choice in case of one disc only
            return choice([AI.LINE, AI.COLUMN, AI.DIAGONAL_UP])

    def check_blocking(self, g, right_end, left_end, column_status):
        """
        check if there is a disc to 'catch' the disc we would like to
        insert, so it wont fall further down, in addition checks the spot is
        not occupied
        :param g: Game object
        :param right_end: right end coordinate - tuple
        :param left_end: left end coordinate - tuple
        :param column_status: dict contains columns and number of discs in
        each column
        :return: integer between 1-7
        """
        right_row = right_end[0]
        right_column = right_end[1] + 1
        # column adjustment between 0 - 6 to 1 - 7
        left_row = left_end[0]
        left_column = left_end[1] + 1
        # column adjustment between 0 - 6 to 1 - 7
        if right_column < 8 and -1 < right_row < 6:
            # check if the height of the discs in a specific column match the
            # move we want
            if column_status[right_column] == (g.BOARD_ROW - right_row - 1):
                return right_column
        if left_column > 0 and -1 < left_row < 6:
            if column_status[left_column] == (g.BOARD_ROW - left_row - 1):
                return left_column

    def operate_move(self, g, right_end, left_end,
                     column_status, func):
        """
        performs the actual move
        :param g: Game object
        :param right_end: right end coordinate - tuple
        :param left_end: left end coordinate - tuple
        :param column_status: dict contains columns and number of discs in
        each column
        :param func: func to perform the next move
        :return: True if func performed, None otherwise
        """
        check_block = self.check_blocking(g, right_end, left_end,
                                          column_status)
        if check_block:
            # perform the func
            choose_button = func(check_block)
            choose_button('click')
            return True

    def set_last_move(self, last_play):
        """
        Class method
        :param last_play: tuple (x,y)
        :return: None
        """
        self.__my_last_play = last_play

###########################################################################
# FILE : four_in_a_row.py
# WRITER : Lior Paz, lioraryepaz, 206240996
# | Eran Gilead, eran.gilead, 203344130
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION : Contains Gui Class, comunication implementation, main file to
# run the program
###########################################################################

import sys
# to choose a cool text
import tkinter as tk
# import game to create object Game
from copy import deepcopy
# to copy the board list in full
from random import choice
# to read files from cmd
from communicator import Communicator
# import tk to do GUI
from game import Game
# import Communicator to create object type communicator
from ai import AI
# import class AI to create object AI

TITLE = 'Fruits In A Row'
# the name of our super coolfragelistic appetizing game ;)
ARGUMENT_WITH_IP = 3
# number of arguments expected to receive from client
ARGUMENT_WITHOUT_IP = 2
# number of argument expected to receive from server
ERROR_MSG = 'illegal program arguments'
# the message shown when one or more of the arguments given are not right
MAX_PORT = 65536
# top range of values our port can have plus 1
MIN_PORT = 999
# bottom range of values our port can have plus 1
HUMAN = 'human'
# the parameter expected to be as "is_human" field
AI_FACTOR = 'ai'
# the parameter expected to be as "is_human" field


class Gui:
    """implements user interface for Game class board using python tkinter
    module and binds actions to Communication class in order to enable
    network games"""
    DRAW_MSG = "IT'S A DRAW"
    # the message shown in case of a draw
    PLAYER_2_WON = "The Red Cherry \n Has Won!!!"
    # the message shown in case player_two wins
    PLAYER_1_WON = "The Green Apple \n Has Won!!!"
    # the message shown in case player_one wins
    FONT_SIZE = 35
    # the font size the messages are shown
    FONT = "Rockwell Extra Bold"
    # the font we're using
    BORDER_COLOR = "hot pink"
    # the color we choose to use to emphasize a sweet victory
    BORDER_THICK = "7"
    # the boarder width around our favorite fruits in the winning row
    WAITING_TEXT = ['Wait For Your \n Turn', "If You Lose \n You're Dead",
                    "You're So Close!", "Why Are You \n So BAD :(",
                    "Your're \n My HERO!"]
    # the text shown when you need to wait for the other player
    FONT_BOLD = 'bold'
    GREEN = 'yellow green'
    # images directories
    BACKGROUND = 'BACKGROUND.png'
    RED_FINAL = 'RED_FINAL.png'
    GREEN_FINAL = 'GREEN_FINAL.png'
    ARROW_RED = 'ARROW_RED.png'
    ARROW_GREEN = 'ARROW_GREEN.png'
    BLANK = 'BLANK.png'

    def __init__(self, root):
        """
        the constructor of the class creating the information the object has.
        :param root: a tkinter window to shown our graphic
        """
        self.__root = root
        self.__create_images()
        # sets the game images
        self.__top_frame = tk.Frame(self.__root, background=Gui.GREEN)
        # a frame at the top of the window we're showing
        # buttons and user messages
        self.__top_frame.pack(side=tk.TOP)
        self.__am_i_ai = False
        self.__board_create()
        if curr_game.get_who_am_i() is Game.PLAYER_ONE:
            self.__button_frame_create()
        else:
            self.__create_waiting_frame()

    def __create_images(self):
        """
        sets the images for each parameter they belong to
        :return: None
        """
        self.__background_img = tk.PhotoImage(file=Gui.BACKGROUND)
        self.__player_1_img = tk.PhotoImage(file=Gui.RED_FINAL)
        self.__player_2_img = tk.PhotoImage(file=Gui.GREEN_FINAL)
        self.__arrow_button_red = tk.PhotoImage(file=Gui.ARROW_RED)
        self.__arrow_button_green = tk.PhotoImage(file=Gui.ARROW_GREEN)
        self.__blank_arrow = tk.PhotoImage(file=Gui.BLANK)

    def __button_frame_create(self):
        """
        creates the button frame in the top frame
        :return: None
        """
        self.__button_frame = tk.Frame(self.__top_frame, background=Gui.GREEN)
        self.__button_frame.pack()
        self.__button_lst = [None for _ in range(Game.BOARD_COLUMN)]
        for column in range(len(self.__button_lst)):
            self.__button_create(column)

    def __button_create(self, column):
        """
        creates the buttons in the button frame
        :param column: an integer between 0 to 6 used to differ the buttons
        from one another and connect them to their columns
        :return: None
        """
        self.__button_lst[column] = tk.Button(self.__button_frame,
                                              image=self.__blank_arrow)
        self.__button_lst[column].pack(side=tk.LEFT)
        self.__button_lst[column].bind("<Button-1>",
                                       self.arrow_click(column + 1))
        # column adjustment between 0 - 6 to 1 - 7
        self.__button_lst[column].bind('<Enter>', self.__button_enter(column))
        self.__button_lst[column].bind('<Leave>', self.__button_leave(column))

    def __board_create(self):
        """
        creates the board as a mat 6X7 frames with the background picture in
        each frame and the top left coordinate is (0,0)
        :return: None
        """
        self.__board = deepcopy(curr_game.get_board())
        for (i, row) in enumerate(self.__board):
            frame = tk.Frame(self.__root, background=Gui.GREEN)
            frame.pack(side=tk.TOP)
            for coordinate in range(len(row)):
                self.__board[i][coordinate] = tk.Label(
                    frame, image=self.__background_img, bg=Gui.GREEN)
                self.__board[i][coordinate].pack(side=tk.LEFT)

    def set_ai(self):
        """
        change the parameter am_i_ai from false to true and if it's the
        first turn in the game it tels the ai to do it
        :return: None
        """
        self.__am_i_ai = True
        if curr_game.get_who_am_i() == curr_game.PLAYER_ONE:
            ai.find_legal_move(curr_game, self.arrow_click)
            ai.set_last_move(curr_game.get_last_disc())

    def get_am_i_ai(self):
        """
        :return: true or false according to the parameter of the class
        """
        return self.__am_i_ai

    def __create_waiting_frame(self):
        """
        creates and shows the frame of the text message shown when waiting for
        your turn
        :return: None
        """
        self.__waiting_label = tk.Label(self.__top_frame, text=choice(
            Gui.WAITING_TEXT), font=(Gui.FONT, Gui.FONT_SIZE,
                                     Gui.FONT_BOLD), bg=Gui.GREEN)
        self.__waiting_label.pack()

    def arrow_click(self, column):
        """
        have the function we want to bind to the button and the number of
        column it's needs to work for
        :param column: an integer between 1 - 7
        :return: function with a permanent column number to make_move by
        """

        def turn(event):
            """
            the action the button should do when pressed
            make_move, update board and gui check if the game has ended,
            sends the message with the column we inserted our player
            :param event: clicked button
            :return: if not crush: returns the winning status except when
            illegal move than returns none
            """
            try:
                curr_game.make_move(column - 1)
                x, y = curr_game.get_last_disc()
                self.__board[x][y].configure(
                    image=self.__get_board_image(x, y))
                won_lst = curr_game.check_status(curr_game.get_last_disc())
                status = curr_game.get_winner()
                curr_game.set_current_player()
                if status is not None:
                    self.search_for_winners(status, won_lst)
                if curr_game.get_current_player() != curr_game.get_who_am_i():
                    communicator.send_message(str(column))
                    self.__button_frame.destroy()
                    if status is None:
                        self.__create_waiting_frame()
                return status
            except:
                return

        return turn

    def __button_enter(self, column):
        """
        the function our button needs to have when the event enter happens
        separate the actions to a specific button by column
        :param column: number between 0 - 6
        :return: the func making our button glow
        """

        def glowing_arrow(event):
            """
            change the image of the button to the correct image according to
            the player
            :param event: when button entered
            :return: None
            """
            self.__button_lst[column].configure(
                image=self.__get_button_image())

        return glowing_arrow

    def __button_leave(self, column):
        """
        the function our button needs to have when the event leave happens
        separate the actions to a specific button by column
        :param column: number between 0 - 6
        :return: the func making our button glow
        """

        def glowing_arrow(event):
            """
            change the image of the button to the default
            :param event: when button leave
            :return: None
            """
            self.__button_lst[column].configure(image=self.__blank_arrow)

        return glowing_arrow

    def __get_board_image(self, x, y):
        """
        checks which image to put in (x,y) on board
        :param x: row number between 0-5
        :param y: column number between 0-6
        :return: the right image
        """
        if curr_game.get_player_at(x, y):
            return self.__player_1_img
        else:
            return self.__player_2_img

    def __get_button_image(self):
        """
        checks which image to put as the current player arrow
        :return: the arrow image
        """
        if curr_game.get_current_player():
            return self.__arrow_button_red
        else:
            return self.__arrow_button_green

    def search_for_winners(self, status, won_list):
        """
        checks if the game situation is a draw or player_one/two wins making
        the wining player in the row shown and show the right text
        :param status: the game winning situation - 0-1 for Player ONE &
        Player TWO, 2 for DRAW, None for no win
        :param won_list: the list of tuples of our fruits champions
        :return: None
        """
        self.__button_frame.destroy()
        if status == Game.DRAW:
            won_text = Gui.DRAW_MSG
        elif status == Game.PLAYER_ONE:
            won_text = Gui.PLAYER_1_WON
            self.__win_glow(won_list)
        elif status == Game.PLAYER_TWO:
            won_text = Gui.PLAYER_2_WON
            self.__win_glow(won_list)
        end_label = tk.Label(self.__top_frame, text=won_text,
                             font=(Gui.FONT, Gui.FONT_SIZE, Gui.FONT_BOLD),
                             bg=Gui.GREEN)
        end_label.pack()

    def __win_glow(self, won_lst):
        """
        making the border of the wining images wider and in a beautiful color
        :param won_lst: list of tuples of coordinates of the wining images
        :return: None
        """
        for coordinate in won_lst:
            x, y = coordinate
            self.__board[x][y].config(highlightbackground=Gui.BORDER_COLOR,
                                      highlightthickness=Gui.BORDER_THICK)

    def shift_turn(self, column):
        """
        the class method to be played when reciving a message and board
        update is needed
        :param column: the number of column between 0-6 to put the opponents
        player
        :return: None
        """
        self.__waiting_label.destroy()
        update_turn = self.arrow_click(column)
        status = update_turn('column')
        if status is None:
            self.__button_frame_create()
        if self.__am_i_ai:
            if status is None:
                ai.find_legal_move(curr_game, self.arrow_click)
                ai.set_last_move(curr_game.get_last_disc())


def sys_reading():
    """
    checking if the sys given are legal and sets the is_human, port, ip
    :return: is_human - string, port - str, ip - None or str
    """
    arguments_length = len(sys.argv)
    if (arguments_length < ARGUMENT_WITHOUT_IP + 1) or (
        arguments_length > ARGUMENT_WITH_IP + 1):
        print(ERROR_MSG)
        return False
    is_human = sys.argv[1]
    if is_human != AI_FACTOR and is_human != HUMAN:
        print(ERROR_MSG)
        return False
    port = int(sys.argv[2])
    if not MIN_PORT < port < MAX_PORT:
        print(ERROR_MSG)
        return False
    if arguments_length == ARGUMENT_WITH_IP + 1:
        ip = sys.argv[3]
    else:
        ip = None
    return is_human, port, ip


def my_turn(column):
    """
    calls the Gui method of updating the last opponents move
    :param column: number between 0-6 received from the opponent
    :return: None
    """
    gui.shift_turn(int(column))


if __name__ == '__main__':
    sys_lst = sys_reading()
    if sys_lst:
        is_human, port, ip = sys_lst
        root = tk.Tk()
        communicator = Communicator(root, port, ip)
        communicator.connect()
        communicator.bind_action_to_message(my_turn)
        # the function to use when receiving a message
        if ip is None:
            curr_game = Game()
            curr_game.set_player(Game.PLAYER_ONE)
        else:
            curr_game = Game()
            curr_game.set_player(Game.PLAYER_TWO)
        root.title(TITLE)
        root.resizable(width=False, height=False)
        # making our root size fixed
        gui = Gui(root)
        if is_human == AI_FACTOR:
            ai = AI()
            gui.set_ai()
            # change gui.am_i_ai to True
        root.configure(background=Gui.GREEN)
        root.mainloop()

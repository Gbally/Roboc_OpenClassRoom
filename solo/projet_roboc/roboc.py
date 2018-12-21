#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# =============================================================================
#            Roboc - OpenClassroom Project
# =============================================================================
# PROJECT : OpenClassroom - section 3
# FILE : roboc.py
# DESCRIPTION :
"""
Requirements:
Python 3

========= ============== ======================================================
Version   Date           Comment
========= ============== ======================================================
0.1.0     2018/10/15     Creation
0.1.1     2018/12/10     Fixed: Crash when playing to a second game
0.2.0     2018/12/11     Added: Multiple move
0.2.1     2018/12/11     Some bug fixed
========= ============== ======================================================
"""

# [IMPORTS]--------------------------------------------------------------------
import os
import time
import re

from labyrinthe import Labyrinth

# [MODULE INFO]----------------------------------------------------------------
__author__ = 'Guillaume Bally'
__date__ = '2018/12/11'
__version__ = '0.2.1'
__maintainer__ = 'Guillaume Bally'

# [GLOBALS] -------------------------------------------------------------------
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
script = Labyrinth()

GAME = ""
LIST_DIRECTION = ["North: N", "East:  E", "South: S", "West:  W",
                  "Save:  Q", "Save and quit: Z"]

RIGHT = "E"
LEFT = "O"
UP = "N"
DOWN = "S"
SAVE = "Q"
S_Q = "Z"


# [Functions]-------------------------------------------------------------------
def saved_game():
    """
    Wrapper for saved games
    """
    global GAME
    GAME = "SAVED"

    maps = read_maps("maps/saves")
    map_number = len(maps)

    if map_number > 0:
        universal_menu(map_number, maps)

    else:
        print("\nNo maps available")
        time.sleep(1.5)
        main()


def new_game():
    """
    Wrapper for new games
    """
    global GAME
    GAME = "NEW"

    # Loading existing maps and store name and map into a dictionary
    maps = read_maps("maps")
    map_number = len(maps)
    if map_number > 0:
        universal_menu(map_number, maps)

    else:
        print("\nNo maps available")
        time.sleep(1.5)
        main()


def delete_game():
    """
    Wrapper to delete a game
    """
    global GAME
    GAME = "None"

    # Loading existing maps and store name and map into a dictionary
    maps = read_maps("maps/saves")
    map_number = len(maps)

    if map_number > 0:
        head()
        print("{} maps available: \n".format(map_number))
        show_maps_list(map_number, maps)

        user_choice = input("\nWhich one would you like to delete: ")
        try:
            path = "maps/saves/" + ((list(maps.keys()))[int(user_choice)
                                                        - 1]) + ".txt"
            os.remove(path)

            print("\nFile deleted ...")
            time.sleep(1.5)
            main()

        except ValueError:
            print("Something went wrong !!!")
            time.sleep(1.5)
            main()

        except IndexError:
            print("Wrong choice !!!")
            time.sleep(1.5)
            main()

    else:
        print("\nNo maps available")
        time.sleep(1.5)
        main()


def universal_menu(map_number, maps):
    """
    Menu wrapper
    :param map_number: Number of available maps
    :param maps: Maps data
    """
    head()
    print("{} maps available: \n".format(map_number))

    print("Preview map  ------------ 1")
    print("Play a map -------------- 2")
    print("Back to main menu ------- 3")
    print("\nExit ---- Any other input\n")

    user_choice = input("Your choice: ")
    if user_choice == "1":
        preview_map(map_number, maps)

    elif user_choice == "2":
        play_map(map_number, maps)

    elif user_choice == "3":
        main()

    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        exit(0)


def show_maps_list(map_number, maps):
    """
    For decoration and understanding from user, this function will be called
    several times.
    :param map_number: Number of maps available
    :param maps: Dictionary
    :return: Name of maps in a list
    """
    # Ini variables
    cpt = 0
    list_map = []

    # Browse keys of the dictionary and print each keys (name of map)
    for map in maps:
        cpt += 1
        print("Map number [{}/{}]: {}".format(cpt, map_number, map))
        list_map.append(map)

    # Return name of maps in a list
    return list_map


def read_maps(path):
    """
    From the provided path, check if some maps are available, read them
    :param path: Path of folder to look for maps
    :return:
    """
    maps = {}
    for file_name in os.listdir(path):
        if file_name.endswith(".txt"):
            path_maps = os.path.join(path, file_name)
            name_maps = file_name[:-4].lower()  # Remove the .txt - could use
            #  split()
            with open(path_maps, "r") as files:
                content = files.read()
                maps[name_maps] = content

    return maps


def preview_map(map_number, maps):
    """
    Preview map before playing
    :param map_number: Total map available
    :param maps: Map data
    """
    head()
    print("{} maps available: \n".format(map_number))
    list_map = show_maps_list(map_number, maps)

    user_input_1 = input("\nWhich map would you like to see (map"
                         "number): ")
    head()
    int_choice = int(user_input_1)

    if check_crash(int_choice, map_number):

        print("------- {} -------\n".format(list_map[int(user_input_1) - 1]))
        print(maps[list_map[int(user_input_1) - 1]])

        input("\n\nEnter to return to main menu")

        # Go back to previous state
        if GAME == "NEW":
            new_game()
        else:
            saved_game()


def play_map(map_number, maps):
    """
    Wrapper to choose which map to play
    :param map_number: Total map available
    :param maps: Map data
    """
    head()
    print("{} maps available: \n".format(map_number))
    list_map = show_maps_list(map_number, maps)

    user_choice = input("\nWhich map would you like to play (map "
                        "number): ")

    if check_crash(int(user_choice), map_number):
        user_choice_int = int(user_choice) - 1
        # Name of the map
        map_chosen = list_map[user_choice_int]
        # Data of the app
        map_data = maps[map_chosen]

        play(map_chosen, map_data)


def check_crash(int_choice, map_number):
    """
    This check is needed at least two times, so it has been wrapped into a
    function
    :param int_choice: User choice converted to a int
    :param map_number: Total map available
    :return: True if OK
    """
    # Check if input is only an int and if it is in the range of total map
    if isinstance(int_choice, int) and \
            (int_choice in range(map_number + 1)):
        return True

    else:
        print("Input not a number or out of range !!!")
        print("Wait 2seconds")
        time.sleep(2)

        # Go back to previous state
        if GAME == "NEW":
            new_game()
        else:
            saved_game()


def play(map_chosen, map_data):
    """
    Play map function
    :param map_chosen: Map name
    :param map_data: Map data
    """
    rules()
    # Reset and clean value sent to Labyrinth() to avoid crashes
    script.__init__()

    script.init(map_chosen, map_data)

    while True:

        head()
        print(script.__repr__())

        for i in LIST_DIRECTION:
            print(i)

        direction = input("\nYour choice: ")
        pattern = "(?<=[A-Z/a-z])\d"
        moves = re.search(pattern, direction)

        try:
            # Which direction has been entered by user
            if direction.upper() == RIGHT:
                result_move = script.move_right()
                script.save()

            elif direction.upper() == LEFT:
                result_move = script.move_left()
                script.save()

            elif direction.upper() == UP:
                result_move = script.move_up()
                script.save()

            elif direction.upper() == DOWN:
                result_move = script.move_down()
                script.save()

            elif direction.upper() == SAVE:
                script.save()
                main()

            elif direction.upper() == S_Q:
                script.save()
                os.system('cls' if os.name == 'nt' else 'clear')
                exit(0)

            # Regex - direction and number of move
            elif moves.group(0):
                i = 0
                if direction[:1].upper() == RIGHT:
                    while i in range(int(moves.group(0))):
                        result_move = script.move_right()
                        win_check(result_move)
                        i += 1

                    script.save()

                elif direction[:1].upper() == LEFT:
                    while i in range(int(moves.group(0))):
                        result_move = script.move_left()
                        win_check(result_move)
                        i += 1
                    script.save()

                elif direction[:1].upper() == UP:
                    while i in range(int(moves.group(0))):
                        result_move = script.move_up()
                        win_check(result_move)
                        i += 1

                    script.save()

                elif direction[:1].upper() == DOWN:
                    while i in range(int(moves.group(0))):
                        result_move = script.move_down()
                        win_check(result_move)
                        i += 1

                    script.save()

            win_check(result_move)

        except AttributeError:

            print("\33[1m\33[91m{}\033[0m is not a valid "
                  "command".format(direction))

            time.sleep(2)


def win_check(result_move):
    """
    Function wrapped due to many use
    :param d: Return of script.move_XXXX()
    """
    if result_move == "End":
        head()
        # Game finished, delete current game
        script.delete_save()
        print("\33[1m\33[91mCongratulation\033[0m")
        print("\33[1mYou escaped\033[0m")
        input("\n\nPress any key to continue")
        main()

    else:
        pass


def rules():
    """
    Display rules before starting a game
    """
    head()
    print("\33[1m*--- How to play ---*\033[0m\n")
    print("The following command allows to control the direction of the "
          "robot.\n")
    for i in LIST_DIRECTION[:4]:
        print("To the {}".format(i))
    print("\nYou can also move add the number of move to do in the same "
          "direction by adding a number from 0 to 9 after the direction:\n")
    print("Examples: S9 - N2 - E0 (Useless but you are a free robot)\n\n")
    input("Press ENTER to continue ...")



def head():
    """
    Function: For better looking...in my opinon =)
    return: N/A
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-----------------------------------------")
    print("|               \33[1m Roboc \033[0m                 |")
    print("| A labyrinth game - From OpenClassRoom |")
    print("-----------------------------------------\n")


def main():
    """
    main
    """
    head()
    print("New game -------------- 1")
    print("Saved game ------------ 2")
    print("Delete saved game ----- 3")
    print("\nExit ---- Any other input")

    user_choice = input("\nYour choice: ")

    if user_choice == "1":
        new_game()

    elif user_choice == "2":
        saved_game()

    elif user_choice == "3":
        delete_game()

    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        exit(0)


# [MAIN]-----------------------------------------------------------------------
if __name__ == '__main__':
    main()

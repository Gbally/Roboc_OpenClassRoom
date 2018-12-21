#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# =============================================================================
#            Roboc - OpenClassroom Project
# =============================================================================
# PROJECT : OpenClassroom - section 3
# FILE : labyrinthe.py
# DESCRIPTION :
"""
Requirements:
python 3

========= ============== ======================================================
Version   Date           Comment
========= ============== ======================================================
0.1.0     2018/10/15     Creation
========= ============== ======================================================
"""

# [IMPORTS]--------------------------------------------------------------------
import os
import copy

# [MODULE INFO]----------------------------------------------------------------
__author__ = 'Guillaume Bally'
__date__ = '2018/12/10'
__version__ = '0.1.0'
__maintainer__ = 'Guillaume Bally'

# [GLOBALS] -------------------------------------------------------------------
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


# [CLASS]----------------------------------------------------------------------
class Labyrinth:

    def __init__(self,):
        self.name = ""
        self.height = 1
        self.length = 0
        self.grid = ""
        self.grid_intact = ""
        self.robot = ""
        self.coordone_robot_ori = ""
        self.exit = ""

    def init(self, name, grid):
        self.name = name
        self.grid = self.__init_labyrinth(grid)
        self.grid_intact = copy.deepcopy(self.grid)
        self.robot = self.__init_element("X")
        self.coordone_robot_ori = self.robot
        self.exit = self.__init_element("U")

    def __init_labyrinth(self, grid):
        """
        Create an Array from the labyrinth grid in 2D
        :param grid: The labyrinth to process
        :return: Array of the labyrinth
        """

        # Calcul grid dimension
        for i in grid:
            # Once we reach the end of the line, we find '\n'
            if i == "\n":
                self.height += 1
                self.length = 0
            else:
                # Add one in length as long as we do not reach the end of
                # the line
                self.length += 1

        # 2D list
        array = [[0 for _ in range(self.length)] for _ in range(self.height)]

        i = 0
        k = 0

        while i < self.height:
            j = 0

            while j < self.length:

                if grid[k] is not "\n":
                    array[i][j] = grid[k]
                    j += 1
                k += 1

            i += 1

        return array

    def __init_element(self, element):
        """
        Init of element's position
        :param element:
        :return: Coordinate of the element
        """
        i = 0

        while i < self.height:
            # Ini and reset j every time the end of the row is reached
            j = 0

            while j < self.length:

                if self.grid[i][j] == element:
                    return (i, j)
                j += 1

            i += 1

    def __repr__(self):
        """
        Put the labyrinth into a string to be easily printed
        :return: Labyrinth into a string
        """

        i = 0
        j = 0
        string = ""

        while i < self.height:
            j = 0
            while j < self.length:
                string += self.grid[i][j]
                j += 1
            string += "\n"
            i += 1

        return string

    def move_up(self):
        """
        Move up the robot
        :return: Map updated
        """
        return self.__move_robot(self.robot[0] - 1, self.robot[1])

    def move_down(self):
        """
        Move down the robot
        :return: Map updated
        """
        return self.__move_robot(self.robot[0] + 1, self.robot[1])

    def move_left(self):
        """
        Move left the robot
        :return: Map updated
        """
        return self.__move_robot(self.robot[0], self.robot[1] - 1)

    def move_right(self):
        """
        Move right the robot
        :return: Map updated
        """
        return self.__move_robot(self.robot[0], self.robot[1] + 1)

    def __move_robot(self, x, y):
        """
        Check the next robot's position -
        :param x: X position to check
        :param y: Y position to check
        :return: Map updated
        """
        if self.grid[x][y] == "O":
            pass
            # print("\33[1mThis is a wall, you can got go through")
            # print("\33[1mYou are not a ghost\n\33[0m")

        else:
            # self.grid[self.robot[0]][self.robot[1]] = " "
            self.grid = copy.deepcopy(self.grid_intact)
            self.grid[self.coordone_robot_ori[0]][
                self.coordone_robot_ori[1]] = " "
            self.grid[x][y] = "X"

            self.robot = (x, y)

        self.__print_labyrinth()

        # If the robot is at the same position as the exit, user win the game
        if self.robot == self.exit:
            print("You won !!!")
            return "End"

    def __print_labyrinth(self):
        """
        Print the labyrinth
        """
        print(repr(self))

    def save(self):
        """
        Save the labyrinth
        """
        path = os.path.join(
            "maps", "saves", "{}.txt".format(self.name))
        with open(path, "w") as file:
            file.write(str.strip(repr(self)))

    def delete_save(self):
        """
        Delete saved labyrinth
        """
        os.remove(os.path.join(
            "maps", "saves", "{}.txt".format(self.name)))

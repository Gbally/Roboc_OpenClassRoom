#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# =============================================================================
#            Roboc - OpenClassroom Project
# =============================================================================
# PROJECT : OpenClassroom - section 4
# FILE : labyrinth.py
# DESCRIPTION :
"""
Requirements:
python 3

========= ============== ======================================================
Version   Date           Comment
========= ============== ======================================================
0.1.0     2018/12/13     Creation
0.1.1	  2018/12/19	 Fixed: Door disappeared after a player walked
						 through it
========= ============== ======================================================
"""

# [IMPORTS]--------------------------------------------------------------------
import os

from random import randint

# [MODULE INFO]----------------------------------------------------------------
__author__ = 'Guillaume Bally'
__date__ = '2018/12/13'
__version__ = '0.1.0'
__maintainer__ = 'Guillaume Bally'

# [GLOBALS] -------------------------------------------------------------------
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


# [CLASS]----------------------------------------------------------------------
class Labyrinth:

	def __init__(self, name, grid):
		"""
		Init of the class
		:param name: Map name
		:param grid: Map data
		"""
		# For labyrinth initialisation
		self.name = name
		self.height = 1
		self.length = 0
		self.grid = self.__init_labyrinth(grid)
		self.exit = self.__init_element("U")

		# Variable - robot information
		self.robot_1 = '$'
		self.robot_1_coordinate = []
		self.robot_2 = '¥'
		self.robot_2_coordinate = []

		# Variable for comparision when moving
		self.door = "."
		self.wall = "O"
		self.exit_door = "U"
		self.server = None
		self.robot_1_door = False
		self.robot_2_door = False

		# Min distance that must separate each players with the exit
		self.secu_range = 3

# [MAP FUNCTIONS] -------------------------------------------------------------

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

	def __repr__(self, player):
		"""
		Put the labyrinth into a string to be easily printed
		:return: Labyrinth into a string
		"""

		i = 0
		string = ""

		while i < self.height:
			j = 0
			while j < self.length:
				if self.grid[i][j] == player:
					format = "\33[1m{}\033[0m".format(str(self.grid[i][j]))
					string += format
					j += 1
				else:
					string += self.grid[i][j]
					j += 1
			string += "\n"
			i += 1

		return string

	def place_players(self):
		"""
		Wrapper to find coordinate for both players. Calculate positions
		then apply to the map
		"""
		# Player 1
		self.robot_1_coordinate = self._random_place()
		self.grid[int(self.robot_1_coordinate[0])][
			int(self.robot_1_coordinate[1])] = self.robot_1

		# Player 2
		self.robot_2_coordinate = self._random_place()
		self.grid[int(self.robot_2_coordinate[0])][
			int(self.robot_2_coordinate[1])] = self.robot_2

	def _random_place(self):
		"""
		Give a random position
		:return: Return a valid random position
		"""
		while True:
			# Generate random position
			position_y = randint(0, self.length)
			position_x = randint(0, self.height)

			try:
				# Can not be few moves away from the exit
				if abs((position_x + position_y) -
							   (self.exit[0] + self.exit[1])) > \
						self.secu_range:

					# Position needs to be empty
					if self.grid[position_x][position_y] == ' ':
						return [position_x, position_y]
			except:
				pass

# [MOVEMENT] ------------------------------------------------------------------

	def move_up(self, robot, shape, if_player=False):
		"""
		Move up the robot
		:return: Map updated
		"""
		if shape == self.robot_1:
			return self.__move_robot(self.robot_1_coordinate[0] - 1,
									 self.robot_1_coordinate[1],
									 robot, shape, if_player)
		elif shape == self.robot_2:
			return self.__move_robot(self.robot_2_coordinate[0] - 1,
									 self.robot_2_coordinate[1],
									 robot, shape, if_player)

	def move_down(self, robot, shape, if_player=False):
		"""
		Move down the robot
		:return: Map updated
		"""
		if shape == self.robot_1:
			return self.__move_robot(self.robot_1_coordinate[0] + 1,
									 self.robot_1_coordinate[1],
									 robot, shape, if_player)
		if shape == self.robot_2:
			return self.__move_robot(self.robot_2_coordinate[0] + 1,
									 self.robot_2_coordinate[1],
									 robot, shape, if_player)

	def move_left(self, robot, shape, if_player=False):
		"""
		Move left the robot
		:return: Map updated
		"""
		if shape == self.robot_1:
			return self.__move_robot(self.robot_1_coordinate[0],
									 self.robot_1_coordinate[1] - 1,
									 robot, shape, if_player)
		if shape == self.robot_2:
			return self.__move_robot(self.robot_2_coordinate[0],
									 self.robot_2_coordinate[1] - 1,
									 robot, shape, if_player)

	def move_right(self, robot, shape, if_player=False):
		"""
		Move right the robot
		:return: Map updated
		"""
		if shape == self.robot_1:
			return self.__move_robot(self.robot_1_coordinate[0],
									 self.robot_1_coordinate[1] + 1,
									 robot, shape, if_player)
		if shape == self.robot_2:
			return self.__move_robot(self.robot_2_coordinate[0],
									 self.robot_2_coordinate[1] + 1,
									 robot, shape, if_player)

# [MAP UPDATE MOVEMENT] -------------------------------------------------------

	def __move_robot(self, x, y, coordinate_robot, robot_shape,
					 if_player=False):
		"""
		Check the next robot's position -
		:param x: X position to check
		:param y: Y position to check
		:return: Map updated
		"""
		# Move
		if self.grid[x][y] == " ":
			self.update_map(x, y, coordinate_robot, robot_shape)

		# If the robot is at the same position as the exit, user win the game
		elif self.grid[x][y] == self.exit_door:
			print("End of game")
			message = "\33[1m{} have won the game\033[0m"
			if robot_shape == self.robot_1:
				self.server.send_message_all_clients(
					message.format("player 1"))

			elif robot_shape == self.robot_2:
				self.server.send_message_all_clients(
					message.format("player 2"))

			# Send command stop server
			self.server.stop_server()

		# In case of a door, player will be stopped by it.
		elif self.grid[x][y] == self.door:
			self.update_map(x, y, coordinate_robot, robot_shape)
			if robot_shape == self.robot_1:
				self.robot_1_door = True
				return "Door"

			elif robot_shape == self.robot_2:
				self.robot_2_door = True
				return "Door"

		# If robot is
		elif self.grid[x][y] == self.wall:
			if if_player:
				self.update_map(x, y, coordinate_robot, robot_shape)
			else:
				return "Wall"

		elif robot_shape == self.robot_1 and self.grid[x][y] == self.robot_2:
			return "Player"

		elif robot_shape == self.robot_2 and self.grid[x][y] == self.robot_1:
			return "Player"

	def update_map(self, x, y, coordinate_robot, robot_shape):
		"""
		Update map - player movement, door, wall
		:param x: Next x position
		:param y: Next y position
		:param coordinate_robot: Current robot position
		:param robot_shape: Shape of the robot
		"""
		if robot_shape == self.robot_1:
			if self.robot_1_door:
				self.grid[coordinate_robot[0]][coordinate_robot[1]] = \
					self.door
				self.robot_1_door = False
				print(self.door)
			else:
				self.grid[coordinate_robot[0]][coordinate_robot[1]] = " "

		elif robot_shape == self.robot_2:
			if self.robot_2_door:
				self.grid[coordinate_robot[0]][coordinate_robot[1]] = \
					self.door
				self.robot_2_door = False
				print(self.door)
			else:
				self.grid[coordinate_robot[0]][coordinate_robot[1]] = " "

		self.grid[x][y] = robot_shape

		if robot_shape == self.robot_1:
			self.robot_1_coordinate = (x, y)

		elif robot_shape == self.robot_2:
			self.robot_2_coordinate = (x, y)

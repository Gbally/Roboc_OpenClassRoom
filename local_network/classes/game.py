#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# =============================================================================
#            Roboc - OpenClassroom Project
# =============================================================================
# PROJECT : OpenClassroom - section 4
# FILE : game.py
# DESCRIPTION :
"""
Requirements:
python 3

========= ============== ======================================================
Version   Date           Comment
========= ============== ======================================================
0.1.0     2018/12/13     Creation
0.2.0	  2018/12/19	 Player can not be placed within 3 blocks from the exit
========= ============== ======================================================
"""

# [IMPORTS]--------------------------------------------------------------------
import os
import time
import re

# [MODULE INFO]----------------------------------------------------------------
__author__ = 'Guillaume Bally'
__date__ = '2018/12/13'
__version__ = '0.1.0'
__maintainer__ = 'Guillaume Bally'

# [GLOBALS] -------------------------------------------------------------------


# [CLASS]----------------------------------------------------------------------
class Game:

	def __init__(self, path):
		"""
		Init of the class
		:param path: Path of folder
		"""
		self.players_ready = False
		# self.game_in_progress = False

		self.path_map = path + "/map"
		# self.path_map_save = self.path_map + "/Save"

		# self.save_available = self._map_available(self.path_map_save)
		self.map_available = self._map_available(self.path_map)

		self.player_1 = None  # Change from False
		self.player_2 = None  # Change from False

		# Used for the logic of the game
		self.direction = ["N", "E", "S", "O"]
		self.player_1_playing = False
		self.player_2_playing = False

		# Variable for comparision when moving
		self.up = "N"
		self.down = "S"
		self.right = "E"
		self.left = "O"

	def _map_available(self, path):
		"""
		Check if maps are available
		:param path: Path to directory
		:return: List of maps name
		"""
		list_map = []
		for f in os.listdir(path):

			# Only .txt files will be taken into account
			if f.endswith('.txt'):
				list_map.append(f[:-4])

			else:
				pass

		# False if nothing found
		return list_map

	def select_map(self):
		"""
		Menu to select the desired map
		:return: Valid answer
		"""
		# Display list of maps
		i = 1
		map_number = len(self.map_available)

		# Display available maps
		print("Map available:")
		for map in self.map_available:
			print("Map {}: {}".format(i, map))
			time.sleep(0.1)
			i += 1

		# Check that the answer is correct
		while True:
			server_choice = input("Your choice [0-9]: ")
			try:
				answer = int(server_choice)
				if answer in range(1, int(map_number) + 1):

					print("\n{} will be played".format(
						self.map_available[answer - 1]))
					print("Server will start listening for clients in 2 "
						  "seconds")
					time.sleep(2)
					return answer

				else:
					print("\n\33[1m\33[91mChoice not in range\033[0m")

			except ValueError:
				print("\n\33[1m\33[91mNot a valid character, only numbers !\033[0m")

	# def read_maps(self, path):
	# 	"""
	# 	From the provided path, check if some maps are available, read them
	# 	:param path: Path of folder to look for maps
	# 	:return:
	# 	"""
	# 	maps = {}
	# 	for file_name in os.listdir(path):
	# 		if file_name.endswith(".txt"):
	# 			path_maps = os.path.join(path, file_name)
	# 			name_maps = file_name.split('.')[0].lower()
	#
	# 			with open(path_maps, "r") as files:
	# 				content = files.read()
	# 				maps[name_maps] = content
	#
	# 	print(type(maps.keys()))
	# 	return maps

	def start_game(self, server, labyrinth):
		"""
		Update players information (from server) and send a message to each
		client to trigger start game
		"""
		self.player_1 = server.clients_connected[0]
		self.player_2 = server.clients_connected[1]

		server.send_message(self.player_1,
							"You are {} on the map".format(labyrinth.robot_1))
		server.send_message(self.player_2,
							"You are {} on the map".format(labyrinth.robot_2))
		time.sleep(0.1)

	def players_answers(self, server, labyrinth):
		"""
		Launch per tour, select who is playing
		:param server:
		:param labyrinth:
		:return:
		"""
		self.player_1_playing = True
		self.player_2_playing = False

		server.send_message_all_clients("CLEAN")

		time.sleep(0.1)
		# server.send_message(self.player_1,
		# 					labyrinth.__repr__(labyrinth.robot_1))
		server.send_message(self.player_2,
							labyrinth.__repr__(labyrinth.robot_2))
		try:
			server.send_message(self.player_1,
								labyrinth.__repr__(labyrinth.robot_1))
			# Player 1 start playing
			while self.player_1_playing:
				time.sleep(0.1)
				server.send_message(self.player_1, "TURN")
				msg = self.player_1.recv(server.MSG_LG).decode()
				if self.answer_move(server,
									msg,
									labyrinth,
									"1",
									labyrinth.robot_1):
					self.player_1_playing = False
					self.player_2_playing = True

					# Print map on the serve side
					print(labyrinth.__repr__("P"))
					time.sleep(0.1)

			# Then player 2 plays
			server.send_message(self.player_2, "CLEAN")
			time.sleep(0.1)
			server.send_message(self.player_2,
								labyrinth.__repr__(labyrinth.robot_2))
			while self.player_2_playing:
				time.sleep(0.1)
				server.send_message(self.player_2, "TURN")
				msg = self.player_2.recv(server.MSG_LG).decode()
				if self.answer_move(server,
									msg,
									labyrinth,
									"2",
									labyrinth.robot_2):
					self.player_1_playing = True
					self.player_2_playing = False

					# Print map on the serve side
					print(labyrinth.__repr__("P"))

			return True

		except OSError:
			# Catch crash error when player quit game
			print("")

	def answer_move(self, server, msg, labyrinth, robot_coordinate_conf, shape):
		"""
		From player message, use the correct function to move it's robot on
		the map
		:param server: Server
		:param msg: Player message
		:param labyrinth: Labyrinth
		:param robot_coordinate_conf: Robot coordinate
		:param shape: Shape of the robot
		:return: True
		"""
		pattern = "(^['M','P','m','p']?)(['N','S','E','O''n','s','e','o']" \
				  "{1})([1-9]*$)"
		moves = re.match(pattern, msg)
		robot_coordinate = ""
		result = ""

		labyrinth.server = server

		if robot_coordinate_conf == "1":
			robot_coordinate = labyrinth.robot_1_coordinate
		elif robot_coordinate_conf == "2":
			robot_coordinate = labyrinth.robot_2_coordinate

		if msg.upper() == self.up:
			result = labyrinth.move_up(robot_coordinate, shape)

		elif msg.upper() == self.down:
			result = labyrinth.move_down(robot_coordinate, shape)

		elif msg.upper() == self.right:
			result = labyrinth.move_right(robot_coordinate, shape)

		elif msg.upper() == self.left:
			result = labyrinth.move_left(robot_coordinate, shape)

		if not self.check_obstacle(result):
			return True

		# Quit game
		elif msg.upper() == "Q":
			server.stop_server()

		elif "P" in msg.upper():
			if msg[1].upper() == self.up:
				result = labyrinth.move_up(robot_coordinate, shape, True)

			elif msg[1].upper() == self.down:
				result = labyrinth.move_down(robot_coordinate, shape, True)

			elif msg[1].upper() == self.right:
				result = labyrinth.move_right(robot_coordinate, shape, True)

			elif msg[1].upper() == self.left:
				result = labyrinth.move_left(robot_coordinate, shape, True)

			if not self.check_obstacle(result):
				return True

		elif "M" in msg.upper():
			if msg[1].upper() == self.up:
				result = labyrinth.move_up(robot_coordinate, shape, True)

			elif msg[1].upper() == self.down:
				result = labyrinth.move_down(robot_coordinate, shape, True)

			elif msg[1].upper() == self.right:
				result = labyrinth.move_right(robot_coordinate, shape, True)

			elif msg[1].upper() == self.left:
				result = labyrinth.move_left(robot_coordinate, shape, True)

			if not self.check_obstacle(result):
				return True

		# If player wants to make many moves
		elif moves.group(3):
			i = 0
			while i in range(int(moves.group(3))):
				time.sleep(0.1)

				# Update at every loop
				if robot_coordinate_conf == "1":
					robot_coordinate = labyrinth.robot_1_coordinate
				elif robot_coordinate_conf == "2":
					robot_coordinate = labyrinth.robot_2_coordinate

				if self.up in msg.upper():
					result = labyrinth.move_up(
						robot_coordinate, shape)
					i += 1

				elif self.down in msg.upper():
					result = labyrinth.move_down(
						robot_coordinate, shape)
					i += 1

				elif self.right in msg.upper():
					result = labyrinth.move_right(
						robot_coordinate, shape)
					i += 1

				elif self.left in msg.upper():
					result = labyrinth.move_left(
						robot_coordinate, shape)
					i += 1

				if not self.check_obstacle(result):
					return True

		return True

	def check_obstacle(self, result):
		"""
		From the result message, figure out if a move a allowed, mainly used
		to exit the loop of many moves
		:param result: Result message from every move
		:return: True if ok, False if obstacle
		"""
		if result == "Wall":
			print("Wall has been hit")
			return False

		elif result == "Player":
			print("leapfrog not allowed")
			return False

		elif result == "Door":
			print("Please open the door")
			return False

		return True

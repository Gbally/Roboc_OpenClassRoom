#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# =============================================================================
#            Roboc - OpenClassroom Project
# =============================================================================
# PROJECT : OpenClassroom - section 4
# FILE : server.py
# DESCRIPTION :
"""
Requirements:
python 3

========= ============== ======================================================
Version   Date           Comment
========= ============== ======================================================
0.1.0     2018/10/13     Creation
========= ============== ======================================================
"""

# [IMPORTS]--------------------------------------------------------------------
import time
import os
import copy

from classes.server import Server
from classes.game import Game
from classes.labyrinth import Labyrinth

# [MODULE INFO]----------------------------------------------------------------
__author__ = 'Guillaume Bally'
__date__ = '2018/12/13'
__version__ = '0.1.0'
__maintainer__ = 'Guillaume Bally'

# [GLOBALS] -------------------------------------------------------------------
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
server = Server()
game = Game(DIR_PATH)


# [FUNCTION] ------------------------------------------------------------------
def main():
	"""
	Main function of the server
	:return:
	"""
	server.head()

	# Choose which map to play
	if game.map_available:
		print("Start a new game\n")
		result = game.select_map()
		map_name = game.map_available[int(result) - 1]

		# Get map data
		maps = game.read_maps(game.path_map)
		map_to_process = maps[map_name]

		# Generate map
		labyrinth = Labyrinth(map_name, map_to_process)

		# Place players in random position
		labyrinth.place_players()
		server.head()
	else:
		print("No map available\n")

	# Start server
	server.start_server()

	# Waiting for two players to join
	if server.waiting_for_players():
		game.players_ready = True
		time.sleep(0.1)

	# Start game on client side, message will change game_started to True
	server.send_message_all_clients("START")

	# Always True until the game finishes
	if game.players_ready:
		game.start_game(server, labyrinth)
		loop = True

		while loop: # Game in process
			game.players_answers(server, labyrinth)


if __name__ == "__main__":
	try:
		main()

	except KeyboardInterrupt:
		print("\n\nERROR: Something went wrong")
		server.stop_server()

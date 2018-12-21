#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# =============================================================================
#            Roboc - OpenClassroom Project
# =============================================================================
# PROJECT : OpenClassroom - section 4
# FILE : client_roboc.py
# DESCRIPTION :
"""
Requirements:
python 3

========= ============== ======================================================
Version   Date           Comment
========= ============== ======================================================
0.1.0     2018/10/13     Creation
0.1.1     2018/10/19     Crash message when game was over
========= ============== ======================================================
"""

# [IMPORTS]--------------------------------------------------------------------
import time
import os
import re

from threading import *
from classes.client import Client

# [MODULE INFO]----------------------------------------------------------------
__author__ = 'Guillaume Bally'
__date__ = '2018/12/19'
__version__ = '0.1.1'
__maintainer__ = 'Guillaume Bally'

# [GLOBALS] -------------------------------------------------------------------
CLIENT = Client("localhost", 12800)
MESSAGE = str()


# [FUNCTION] ------------------------------------------------------------------
def communication_server():
	"""
	Server message thread
	"""

	while not CLIENT.game_finished:
		MESSAGE = CLIENT.listen()

		if MESSAGE == "START":
			print("=== Game start ! ===")
			CLIENT.game_started = True

		elif MESSAGE == "CLEAN":
			os.system('cls' if os.name == 'nt' else 'clear')

		elif MESSAGE == "STOP":
			print("Game is Over ! Press ENTER to exit.")
			CLIENT.disconnection()
			CLIENT.game_started = False
			CLIENT.player_turn = False
			exit(0)

		elif MESSAGE == "WAIT":
			print("Waiting for player...")

		elif MESSAGE == "READY":
			print("Press 'c' to start the game.")

		elif MESSAGE == "TURN":
			print("Your turn ! Press'Q' to rage quit.")
			CLIENT.player_turn = True

		else:
			print(MESSAGE)


def player_command():
	"""
	User command thread
	"""

	while not CLIENT.game_finished:
		try:
			msg = input()
		except ValueError:
			exit(0)

		# Player turn
		if not CLIENT.game_started:
			# La partie n'a pas commencé, on envoie le message au serveur.
			CLIENT.send_message(msg)

		elif CLIENT.player_turn:
			# C'est au joueur de jouer, on autorise l'envoie de message.
			if re.match("^['M','P']?['N','S','E','O']{1}[1-9]*$", msg.upper()):
				CLIENT.send_message(msg)
				CLIENT.player_turn = False

			elif msg.upper() == 'Q':
				CLIENT.send_message(msg)
				CLIENT.player_turn = False
			else:
				print("Invalid command")

		# Not player turn
		else:
			pass


# [MAIN] ----------------------------------------------------------------------
def main():
	print("Welcome to Roboc - Openclassroom project")

	# Tentative de connexion au serveur
	while True:
		try:
			CLIENT.start_server()
			break

		except:
			print("\nERROR: Can't reach server.\nRetry in 3 seconds...")
			time.sleep(3)

	# Displayed only at start of the game
	print("---------------------------------------------------")
	print("Rules :")
	print("  Q for rage quit.")
	print("  NESO to move the robot through the labyrinth.")
	print("  You are allowed to make several moves to walk faster")
	print("  Example: E3 - N6")
	print()
	print("  P[+direction] To destroy a wall")
	print("  M[+direction] Create a door in a wall")
	print("")
	print("  You can not jump over the other player")
	print("  Every door will stop you on it")
	print("---------------------------------------------------")
	print(CLIENT.listen())
	# print("DEBUG: PASS")

	# Init thread
	player_command_thread = Thread(target=player_command)
	communication_server_thread = Thread(target=communication_server)

	# Start thread
	player_command_thread.start()
	communication_server_thread.start()

	# Join thread
	player_command_thread.join()
	communication_server_thread.join()


if __name__ == "__main__":
	main()

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
import socket
import select
import time
import os


# [MODULE INFO]----------------------------------------------------------------
__author__ = 'Guillaume Bally'
__date__ = '2018/12/13'
__version__ = '0.1.0'
__maintainer__ = 'Guillaume Bally'

# [GLOBALS] -------------------------------------------------------------------
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


# [CLASS]----------------------------------------------------------------------
class Server:

	def __init__(self):
		"""
		Init of the class
		"""
		# Server config
		self.host = 'localhost'
		self.port = 12800
		self.MSG_LG = 1024

		# Variables
		self.clients_connected = []
		self.clients_to_read = []

		# Separate both players, will be used for the logic of the game
		self.client_1 = None
		self.client_2 = None

	def start_server(self):
		"""
		Start the server roboc
		"""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.host, self.port))
		self.socket.listen(5)

		print("Server launched ...")
		print("Server info: {}, {}".format(self.host, self.port))

	def stop_server(self):
		"""
		Kill server and send stop service to clients
		"""
		print("\nDisconnection...")
		time.sleep(0.1)
		self.send_message_all_clients("STOP")
		time.sleep(0.5)

		print("Kill clients connections")
		for client in self.clients_connected:
			client.close()

		print("Kill sockets")
		self.socket.close()

		input("\nPress ENTER to exit")
		exit(0)

	def waiting_for_players(self):
		"""
		Server need to wait for two clients to be connected in order to start
		the game
		"""
		print("Waiting for clients ...\n")
		total_clients = 0
		new_connection = False

		while True:
			connexions, wlist, xlist = select.select([self.socket],
													 [],
													 [],
													 0.05)

			for connexion in connexions:

				conn, info = connexion.accept()

				self.clients_connected.append(conn)
				total_clients = len(self.clients_connected)
				new_connection = True

				print("Client {} connected".format(info))

				self.send_message_all_clients(
					"Connexion of player {}\n".format(total_clients))

			# Waiting for 2 players to connect
			if new_connection and total_clients >= 2:
				self.send_message_all_clients(
					"{} players are connected.\n".format(total_clients))
				self.send_message_all_clients(
					"When ready, press: 'c'.")
				# self.send_message_all_clients("READY")

			new_connection = False

			# Read clients command
			try:
				self.clients_to_read, wlist, xlist = select.select(
					self.clients_connected, [], [], 0.05)

			except select.error:
				pass

			else:

				for client in self.clients_to_read:
					msg = client.recv(self.MSG_LG).decode()

					if msg.upper() == "C" and total_clients >= 2:
						return True

					if msg.upper() == 'Q':
						print("Stop the game")
						return False

					if total_clients < 2:
						self.send_message(client, "WAIT")
					else:
						self.send_message(client, "READY")

	@staticmethod
	def send_message(client, message):
		"""
		Send a string to desired client
		:param client: Desired client
		:param message: string to be sent
		"""
		try:
			client.send(message.encode())

		except OSError:
			# Catch crash error when player quit game
			print("")

	def send_message_all_clients(self, message):
		"""
		Send a string to all connected clients
		:param message: string to be sent
		"""
		try:
			for client in self.clients_connected:
				client.send(message.encode())

		except OSError:
			# Catch crash error when player quit game
			print("")

	def head(self):
		"""
		Function: For better looking...in my opinon =)
		return: N/A
		"""
		os.system('cls' if os.name == 'nt' else 'clear')
		print("-----------------------------------------")
		print("|               \33[1m Roboc \033[0m                 |")
		print("| A labyrinth game - From OpenClassRoom |")
		print("-----------------------------------------\n")

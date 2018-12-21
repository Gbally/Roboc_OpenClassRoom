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

# [MODULE INFO]----------------------------------------------------------------
__author__ = 'Guillaume Bally'
__date__ = '2018/12/13'
__version__ = '0.1.0'
__maintainer__ = 'Guillaume Bally'

# [GLOBALS] -------------------------------------------------------------------


# [CLASS]----------------------------------------------------------------------
class Client:

	def __init__(self, host_serveur, port_serveur):
		"""
		Init of the class
		:param host_serveur: host
		:param port_serveur: port
		"""
		# Init server info
		self.host = host_serveur
		self.port = port_serveur
		self.code = 1024

		# Init game state
		self.game_started = False
		self.game_finished = False
		self.player_turn = False

		self.server = None

	def start_server(self):
		"""
		Connect to the server
		:return:
		"""

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.connect((self.host, self.port))

		print("Connexion établie avec le serveur sur le port {}".format(
			self.port))

	def disconnection(self):
		"""
		Disconnection to the server
		"""
		if self.server.close():

			print("Successfully disconnected from the server")

	def send_message(self, message):
		"""
		Send message to the server
		:param message: str() - User input
		"""
		try:
			if self.server.send(message.encode()):
				self.player_turn = False

		except OSError:
			# Catch crash error when player quit game
			print("")

	def listen(self):
		"""
		Listen for server message
		"""
		server_msg = self.server.recv(self.code).decode()

		return server_msg

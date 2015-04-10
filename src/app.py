# hello python
name = 'Gideon'
version = 'v0.1'
authors = ('Awal Garg', 'argentum47')
botname = 'Gideon'


# sys internals, bitches

import getpass
from gi.repository import GLib

username = getpass.getuser()
username_safe = GLib.markup_escape_text(username)

import logging
def setup_custom_logger(name):
	logFmt = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
	logHandler = logging.StreamHandler()
	logHandler.setFormatter(logFmt)

	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)
	logger.addHandler(logHandler)
	return logger

logger = setup_custom_logger(name + '_logger')
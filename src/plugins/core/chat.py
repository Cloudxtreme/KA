import random
import app
from gi.repository import Gtk
from utils.response_wrapper import ResponseWrap
import hashlib

emptyAnswers = [
	"Exactly <b>what</b> are you trying to say?",
	"boom boom",
	"I am having a hard time following you...",
	"You sure didn't mean that, now did you? (I didn't really understand it -_-)",
	"Hrm? I missed your message, I guess..."
]

hardcodedanswers = {
	'42': ['I have no more questions.'],
	'will you marry me?': [
		'No.',
		'Not possible.',
		'I think you forgot you are talking to a... virtual being.',
		'Someone won\'t allow  me to...',
		'Not unless you are the person I have been thinking about!',
		'Maaybe?',
		'I would rather not answer that question.',
		],
	'i hate you': ['What did I do? :(', 'Fine!', 'How can I help the situation?', ':(', ':\'('],
	'bye': ['Ok, bye!', 'Cya later!'],
	'who is siri?': ['They say she is some white girl who is meant to be helpful...'],
	'who is cortana?': ['A blue lady who can\'t even...', 'I forgot! :P'],
	'how are you better than siri?': ['By not answering questions like these.'],
	'how are you better than cortana?': ['I am written in Python.', 'I wonder the same.', 'I don\'t chatter much.'],
	'thanks': ['More than welcome!', 'My pleasure :)', 'Anytime.', 'Enjoy!']
}


def get_raw_answer(cmd):
	# so.. uhh
	if (hashlib.sha1(cmd.encode('utf-8')).hexdigest() == '54fb4512f75a1b08eb880520cf0cd0774a99ad6e'):
		# ka...
		return 'Yup, that\'s the name!'
	# she was there
	if (cmd.lower() in hardcodedanswers):
		# at the corner of stairs, probably gliding downwards
		return random.choice(hardcodedanswers[cmd.lower()])
		# and I just arrived
	return random.choice(emptyAnswers)
	# I remember seeing her eyes (and hair (and face))
	# it's been years
	# I can't even...
	# KA!!!
	# :'(

def process(cmd):
	raw_answer = get_raw_answer(cmd)
	response = ResponseWrap()
	response.el("message").set_markup(raw_answer)
	return response.el("message-wrapper")
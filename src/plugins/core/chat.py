import random
import app
from gi.repository import Gtk
from utils.response_wrapper import ResponseWrap

emptyAnswers = [
	"Exactly <b>what</b> are you trying to say?",
	"boom boom",
	"I am having a hard time following you...",
	"You sure didn't mean that, now did you? (I didn't really understand it -_-)",
	"Hrm? I missed your message, I guess..."
]

def get_raw_answer(cmd):
	# my special artificial intelligence bot, fu siri and cortana
	return random.choice(emptyAnswers)

def process(cmd):
	raw_answer = get_raw_answer(cmd)
	response = ResponseWrap()
	response.el("message").set_markup(raw_answer)
	return response.el("message-wrapper")
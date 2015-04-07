import random
import re
# import sys
# sys.path.append('scripts')
# import scripts
import imp

SYSTEM_CMD_PREFIX = '!!'

emptyAnswers = [
	"You feeling unhappy or something?",
	"Hey whatsup?",
	"boom boom",
	"Waiting for your command, sir!",
	"You lookin so good today :S",
	"Hrm? I missed your message, I guess..."
]

commands = {
	'core': {},
	'user': {},
	'adv': {},
	'system': {}
}

class AddCmd:
	@staticmethod
	def core(starts, regex, module):
		commands['core'][starts] = {
			'regex': re.compile(regex),
			'module': module
		}
	@staticmethod
	def system(starts, regex, module):
		commands['system'][starts] = {
			'regex': re.compile(regex),
			'module': module
		}
	@staticmethod
	def user():
		pass
	@staticmethod
	def adv():
		pass

AddCmd.core('google', '^google\s+(?P<query>.+)$', 'google')
AddCmd.core('define', '^define\s+(?P<query>.+)$', 'define')
AddCmd.core('wiki', '^wiki\s+(?P<query>.+)$', 'wiki')
AddCmd.core('nudge', '^nudge\s+(?P<message>.+)\s+(?P<timeStyle>at|in)\s+(?P<time>.+)$', 'nudge')
AddCmd.core('how to', '^how to .+', 'google')
AddCmd.core('what is', '^what is\s+(?P<query>\S+)$', 'define')
AddCmd.core('mdn', '^mdn\s+(?P<query>.+)$', 'mdn')
AddCmd.core('learn', '^learn\s+(?P<cmd>\S+)\s+(?P<definition>.+)$', 'learn')
AddCmd.core('should I', '^should\s+I\s+(?P<query>.+or.+[^?])\?*$', 'choose')
AddCmd.core('urban', '^urban\s+(?P<query>.+)', 'urban')
AddCmd.core('hi gideon', '^hi gideon$', 'greet')
AddCmd.core('joke', '^joke$', 'joke')

AddCmd.system('help', '^help', 'help')
AddCmd.system('listcommands', '^listcommands$', 'listcommands')

def fetchResponse(cmd = ''):
	if not cmd:
		return random.choice(emptyAnswers)

	if (cmd.startswith(SYSTEM_CMD_PREFIX)):
		# load from system command whateva
		return

	# print(getattr(commands['core'], 'google'))
	cmdObj = None
	response = None
	try:
		cmdObj = commands['core'][re.split('\s+', cmd, 1)[0]]
	except:
		pass

	if cmdObj:
		try:
			mod_info = imp.find_module(cmdObj['module'], ['./scripts'])
			mod = imp.load_module(cmdObj['module'], *mod_info)
			func = getattr(mod, 'process')
			response = func(cmd, **cmdObj['regex'].match(cmd).groupdict())
			print(response)
		except AttributeError as e:
			print('Unknown module :/', cmd, e)
		finally:
			if mod_info:
				mod_info[0].close()
		return response
	print("Unable to find module for: Command passed", cmd)
	return False
import random
import re
import imp
import os
import app

SYSTEM_CMD_PREFIX = '!!'

commands = {
	'core': {},
	'user': {},
	'system': {}
}

class AddCmd:
	@staticmethod
	def core(starts, regex, module):
		commands['core'][starts] = {
			'regex': re.compile(regex),
			'module': module,
			'category': 'core'
		}
	@staticmethod
	def system(starts, regex, module):
		commands['system'][starts] = {
			'regex': re.compile(regex),
			'module': module,
			'category': 'system'
		}
	@staticmethod
	def user():
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

def load_cmd_module (name = 'chat', mod_type = 'core'):
	mod_info = None
	module = None
	try:
		mod_info = imp.find_module(name, ['./plugins', os.path.join('./plugins', mod_type)])
		module = imp.load_module(name, *mod_info)
	except Exception as e:
		app.logger.error("Error occured while loading module " + name)
		app.logger.debug(e)
	finally:
		if mod_info:
			mod_info[0].close()
	return module

def is_system_command (cmd = ''):
	return cmd.startswith(SYSTEM_CMD_PREFIX)

def get_cmd_definition (cmd = ''):
	first_word = re.split('\s+', cmd)[0]
	first_two_words = ' '.join(re.split('\s+', cmd)[0:2])

	if first_word in commands['core']:
		return commands['core'][first_word]
	elif first_two_words in commands['core']:
		return commands['core'][first_two_words]
	elif first_word in commands['user']:
		return commands['user'][first_word]
	elif first_two_words in commands['user']:
		return commands['user'][first_two_words]
	elif is_system_command(cmd):
		if first_word in commands['system']:
			return commands['system'][first_word]
		elif first_two_words in commands['system']:
			return commands['system'][first_two_words]
		else:
			return False
	else:
		return False

def process(cmd = ''):
	mod_name = None
	response = None
	cmd_definition = None
	module_obj = None
	
	if not cmd:
		mod_name = 'chat'

	cmd_definition = get_cmd_definition(cmd)
	if cmd_definition:
		module_obj = load_cmd_module(name = cmd_definition['module'], mod_type = cmd_definition['category'])
		if not module_obj:
			app.logger.error("module_obj was not found!")
			app.logger.debug([cmd_definition, "command:" + cmd])
			module_obj = load_cmd_module('boterror', 'core')
		response = module_obj.process(cmd, cmd_definition['regex'].match(cmd).groupdict())
		app.logger.info([cmd_definition['module'], cmd_definition['category'], "returned", response])
	else:
		module_obj = load_cmd_module(name = 'chat', mod_type = 'core')
		response = module_obj.process(cmd)
		app.logger.info(["chat returned", response, "for", cmd])
	return response
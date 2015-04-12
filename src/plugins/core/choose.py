import random
import app
import re
import json
from utils.response_wrapper import ResponseWrap

repeated_query_answers = [
	'I remember answering that already.',
	'My answer won\'t change, ' + app.username_safe + '!',
	'Duplicate question?',
	'Didn\'t like my answer first time?',
	'Why ask the same thing again?'
]

yes_no_answers = [
	'Yeah, sure ' + app.username_safe + ' :)',
	'Definitely!',
	'Not sure if that is the best idea... ' + app.username_safe,
	'Why not?!',
	'Oh, no...',
	'Well, you can... but is it a good idea? No.',
	'I would say, go ahead!',
	'Tough choice, but I say do it, ' + app.username_safe,
	'I might be biased but.. NO!',
	'Eh... no.'
]

quick_answers = [
	'The latter!',
	'The former!',
	'The latter, I say...',
	'I would say, the former, ' + app.username_safe,
	'Er, definitely the first choice',
	'I feel the latter is the best option, ' + app.username_safe
]

person_prefixes = [
	'I say... ',
	'How about, ',
	'I think '
]

mem = {}

def rand_bool(yes = 1, no = 1):
	return bool(random.randrange(2))

def map_personal(person, response, is_quick):
	if is_quick:
		return response
	if rand_bool():
		lperson = person.lower().strip()
		if lperson == 'i':
			return 'You should ' + response
		elif lperson == 'you':
			return 'I should ' + response
		elif lperson.startswith('my'):
			return person.replace('my', 'your') + ' should ' + response
		else:
			return person + ' should ' + response
	else:
		return random.choice(person_prefixes) + response

def chose_from_two(person, query):
	if rand_bool():
		return (random.choice(quick_answers), True)
	return (random.choice(query), False)


def chose_from_list(person, query):
	return random.choice(query)

def make_choice(person, query):
	arr = re.split('\s+or\s+', query)
	arr.sort()

	query_id = json.dumps([person, arr])
	if (query_id in mem):
		return random.choice(repeated_query_answers)
	else:
		mem[query_id] = True
	
	if len(arr) == 1:
		return random.choice(yes_no_answers)
	
	choice = ''
	is_quick = False
	if len(arr) == 2:
		choice, is_quick = chose_from_two(person, arr)
	else:
		choice = chose_from_list(person, arr)

	if choice.lower().startswith('should ' + person.lower()):
		choice = re.sub('(?i)' + re.escape('should ' + person), '', choice)

	return map_personal(person, choice, is_quick)


def process(cmd, person, query = ''):
	choice = make_choice(person, query.strip().rstrip('?').strip())
	response = ResponseWrap()
	response.el("message").set_text(choice)
	return response.el("message-wrapper")
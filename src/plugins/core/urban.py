import json
from utils import request
from gi.repository import Gtk, GLib
from utils.response_wrapper import ResponseWrap
import random
import app

address_lines = [
	'I found the following results for your query, ' + app.username_safe,
	app.username_safe + ', here are some definitions',
	'This is what I found, ' + app.username_safe,
	'Urban dictionary gave the following results, ' + app.username_safe
]

empty_query_answers = [
	'Urban what?',
	'It\'s not like an empty search will give a lot of results, ' + app.username_safe,
	'I am not sure what exactly I have to look up',
	'Urban means urban. No urbaning without urban.',
	'Urban! urban! urban! Sing with me! Urb..',
	'Yo! Urban dictionary is awesome right?'
]

no_results = [
	'I... can\'t find anything about that. Seriously.',
	'There are no urban results for that, ' + app.username_safe,
	'Damn! No results :(',
	'Urban dictionary contains no knowledge of such a word!'
]

def escape(**kwargs):
	# I... uhh... too long
	for key in kwargs:
		kwargs[key] = GLib.markup_escape_text(str(kwargs[key]))

	return kwargs

def get_search_results(query):
	if query == '':
		return random.choice(empty_query_answers)

	resp = json.loads(request.process('http://api.urbandictionary.com/v0/define', data={
		'term' : query,
		}).read().decode())
	
	results = resp['list']
	
	if not results:
		return random.choice(no_results)

	result_markup = random.choice(address_lines) + "\n"
	for res in results:
		escaped_data = escape(
			url = res['permalink'],
			word = res['word'],
			upvotes = res['thumbs_up'],
			downvotes = res['thumbs_down'],
			author = res['author'],
			definition = res['definition'],
			example = res['example']
			)
		result_markup += """
<a href="{url}" title="{url}">{word}</a> <i>Votes: +{upvotes} and -{downvotes}</i>
<small>From {author}:</small>
{definition}
Example: {example}
""".format(**escaped_data)

	return result_markup


def process(cmd = '', query = ''):
	search_results = get_search_results(query)
	response = ResponseWrap('./ui/response/google_results.xml')
	response.el("msg-content").set_markup(search_results)
	return response.el("message-wrapper")
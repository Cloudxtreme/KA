import json
from utils import request
from gi.repository import Gtk, GLib
from utils.response_wrapper import ResponseWrap
import random
import app

username = GLib.markup_escape_text(app.username)

address_lines = [
	'I found the following results for your query, ' + username,
	username + ', here are some links',
	'This is what I found, ' + username,
	'Top Google hits just for you, ' + username
]

empty_query_answers = [
	'Google what?',
	'It\'s not like an empty search will give a lot of results, ' + username,
	'I am not sure what exactly I have to look up',
	'Google? Yes, it is awesome isn\'t it?'
]

no_results = [
	'I... can\'t find anything about that. Seriously.',
	'Even my Google-fu failed, ' + username,
	'Damn! No results :('
]

def get_search_results(query):
	if query == '':
		return random.choice(empty_query_answers)

	resp = json.loads(request.process('http://ajax.googleapis.com/ajax/services/search/web', data={
		'q' : query,
		'v' : 1.0
		}).read().decode())
	
	results = resp['responseData']['results']
	
	if not results:
		return random.choice(no_results)

	result_markup = random.choice(address_lines) + "\n"
	for res in results:
		result_markup += """
<a href="{url}" title="{tooltip}">{title}</a>
<small>@{visibleUrl}</small>
""".format(title=res['title'], url=res['url'], visibleUrl=res['visibleUrl'], tooltip=GLib.markup_escape_text(res['content']))

	return result_markup


def process(cmd = '', query = ''):
	search_results = get_search_results(query)
	response = ResponseWrap('./ui/response/google_results.xml')
	response.el("msg-content").set_markup(search_results)
	return response.el("message-wrapper")
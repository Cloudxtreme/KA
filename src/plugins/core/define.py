import json
import app
from utils import request
from gi.repository.GLib import markup_escape_text as escape
from urllib.parse import urlparse
from utils.response_wrapper import ResponseWrap
from utils import request
import random

MAX_ENTRIES = 2

heading_prefixes = [
	'Here is what I found.',
	'These are the results I extracted, ' + app.username_safe,
	'Checkout the following results',
	'I got these results from a big library, ' + app.username_safe
]

def parse_definitions(results):
	if not 'dictionaryData' in results: return False
	
	ans = {
		'web': '',
		'entries': []
	}
	data = results['dictionaryData'][0]
	if 'webDefinitions' in data:
		_def = data['webDefinitions'][0]
		_ret_data = {
			'sourceurl': escape(_def['sourceUrl']),
			'sourcedomain': urlparse(_def['sourceUrl'])[1],
			'definition': escape(_def['definition'])
		}
		ans['web'] = """<i>From <a href="{sourceurl}" title="{sourceurl}">{sourcedomain}</a>:</i>
{definition}""".format(**_ret_data)
	if 'entries' in data:
		for i, entry in enumerate(data['entries']):
			if i == MAX_ENTRIES: break
			_def = {
				'title': escape(data['queryTerm']),
				'definition': '',
				'class': 'other'
			}
			_def['title'] = escape(entry['headword']) if 'headword' in entry else _def['title']
			_def['title'] += escape(' (' + entry['phonetics'][0]['text'] + ')') if 'phonetics' in entry else ''
			if 'senseFamilies' in entry:
				sense = entry['senseFamilies'][0]['senses'][0]
				_def['concise_definition'] = escape(sense['conciseDefinition'])
				if 'domainClasses' in sense:
					_def['class'] = escape(sense['domainClasses'][0])
			ans['entries'].append("""{title} <i>(Category: {class})</i>
{definition}""".format(**_def))
	return ans

def create_gtk_object(ans):
	ret = ResponseWrap('./ui/response/define.xml')
	if not ans:
		ret.el("heading").set_text("No results found!")
		ret.el("web-definition").destroy()
		ret.el("entries").destroy()
		return ret.el("message-wrapper")
	ret.el("heading").set_markup(random.choice(heading_prefixes))
	if ans['web']:
		ret.el("web-definition").set_markup(ans['web'])
	else:
		ret.el("web-definition").destroy()
	if ans['entries']:
		ret.el("entries").set_markup("May also refer to:\n" + "\n".join(ans['entries']))
	else:
		ret.el("entries").destroy()
	return ret.el("message-wrapper")


def get_results(query):
	return json.loads(request.process('https://content.googleapis.com/dictionaryextension/v1/knowledge/search', data = {
		'language': 'en',
		'key': 'AIzaSyC9PDwo2wgENKuI8DSFOfqFqKP2cKAxxso', # consider getting your own
		'term' : query
	}, headers = {
		'X-Origin': 'chrome-extension:',
		'X-Referer': 'chrome-extension://mgijmajocgfcbeboacabfgobmjgjcoja'
	}).read().decode())

def process(cmd, query):
	answer = parse_definitions(get_results(query.strip()))
	return create_gtk_object(answer)
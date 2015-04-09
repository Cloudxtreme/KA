import json
import sys
from scripts import request
from gi.repository import GLib

def parseMarkup(markup):
	return markup # TODO :P

def process(cmd, query):
	result = json.loads(request.request('http://en.wiktionary.org/w/api.php', data={
		'action' : 'query',
		'format' : 'json',
		'continue': '',
		'prop' : 'extracts',
		'indexpageids' : 'true',
		'titles' : query
		}).read().decode())
	ret = {
		'description': '',
		'heading': "Looking up {query}".format(query=GLib.markup_escape_text(query))
	}
	print(ret)
	for page in result['query']['pages']:
		ret['description']+=parseMarkup(result['query']['pages'][page]['extract'])+"\n"
	return ret
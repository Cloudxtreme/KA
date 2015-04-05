import json
import sys
from request import request

def define(term):
	result = json.loads(request('http://en.wiktionary.org/w/api.php', data={
		'action' : 'query',
		'format' : 'json',
		'continue': '',
		'prop' : 'extracts',
		'indexpageids' : 'true',
		'titles' : term
		}).read().decode())
	for page in result['query']['pages']:
		print(result['query']['pages'][page]['extract'])	

define(' '.join(sys.argv[1:]))
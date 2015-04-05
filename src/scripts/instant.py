# this uses the ddg instant answer api, perfect for a virtual assistant

import json
import sys
import re
from request import request

def instant(term):
	resp = json.loads(re.compile('^DDG.duckbar.add_array\(|\);$').sub('', request('https://duckduckgo.com/a.js', data={
		'q' : term,
		'no_html' : '1',
		'skip_disambig' : '1'
		}).read().decode()))

	if not resp:
		return print("I don't think that is a valid question :/")
	
	data = resp[0]['data']
	for result in data:
		print(result['heading'])
		print(result['abstract'])
		print("Source: {source} | Read more at {url}".format(source=result['source'], url=result['url']))


instant(' '.join(sys.argv[1:]))
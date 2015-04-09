# this uses the ddg instant answer api, perfect for a virtual assistant

import json
import sys
import re
from scripts import request
from gi.repository import GLib

def process(query):
	resp = json.loads(re.compile('^DDG.duckbar.add_array\(|\);$').sub('', request.request('https://duckduckgo.com/a.js', data={
		'q' : term,
		# 'no_html' : '1',
		'skip_disambig' : '1'
		}).read().decode()))

	if not resp:
		return {'description': "I don't think that is a valid question :/", 'heading': 'nothing found!'}
	
	data = resp[0]['data']
	ret = {
		'heading': "Found {num} results for {search}".format(num=len(data), search=GLib.escape_markup_text(query)),
		'description': ''
	}
	for result in data:
		ret.append("{heading}\n{abstract}\nSource: {source} | Read more at <a href=\"{url}\"\n"
			.format(heading=result['heading'], abstract=result['abstract'],
				source=result['source'], url=result['url']))

	return ret
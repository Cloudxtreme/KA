import json
import sys
from scripts import request
from gi.repository import GLib

def process(cmd, query):
	result = json.loads(request.request('http://ajax.googleapis.com/ajax/services/search/web', data={
		'q' : query,
		'v' : 1.0
		}).read().decode())
	ret = {
		'description': '',
		'heading': "Google <b>{query}</b>".format(query=GLib.markup_escape_text(query))
	}
	for res in result['responseData']['results']:
		ret['description'] += "<a href=\"{url}\">{title}</a> <small>@{visibleUrl}</small>\n".format(title=res['title'], url=res['url'], visibleUrl=res['visibleUrl'])
	return ret
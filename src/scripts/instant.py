# this uses the ddg instant answer api, perfect for a virtual assistant

import json
import sys
from request import request

def instant(term):
	resp = json.loads(request('http://api.duckduckgo.com/', data={
		'q' : term,
		'format' : 'json',
		'noredirect' : '1',
		'no_html' : '1',
		'skip_disambig' : '1'
		}).read().decode())
	
	if (not resp['Heading']):
		return print("Couldn't find {}", resp)
	print("{Heading} | (category: {Entity})".format(Heading=resp['Heading'], Entity=resp['Entity']))
	print(resp['AbstractText'])
	print("From {AbstractSource}. Read more at {AbstractURL}".format(AbstractSource=resp['AbstractSource'], AbstractURL=resp['AbstractURL']))

instant(' '.join(sys.argv[1:]))
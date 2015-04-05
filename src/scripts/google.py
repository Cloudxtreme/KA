import json
import sys
from request import request

def google(term):
	result = json.loads(request('http://ajax.googleapis.com/ajax/services/search/web', data={
		'q' : term,
		'v' : 1.0
		}).read().decode())
	for res in result['responseData']['results']:
		print("{title} : {url}".format(title=res['titleNoFormatting'], url=res['url']))

google(' '.join(sys.argv[1:]))
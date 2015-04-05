import json
import sys
from request import request

def wiki(term):
	resp = json.loads(request('http://en.wikipedia.org/w/api.php/', data={
		'action' : 'opensearch',
		'search' : term,
		'limit' : 1,
		'format' : 'json'
		}).read().decode())
	print("{title} : {description}".format(title=resp[1][0], description=resp[2][0]))
	print("Read more at {link}".format(link=resp[3][0]))
	

wiki(' '.join(sys.argv[1:]))
from http.client import HTTPConnection, HTTPSConnection
import urllib.parse

def process(url, data={}, headers={}, method="GET"):

	ua = 'Gedion Pluggable Personal Assistant v0.1 pre-alpha'

	q = urllib.parse.urlencode(data)
	headers['User-Agent'] = ua

	urlparts = urllib.parse.urlparse(url)
	if urlparts[0] == 'https':
		h = HTTPSConnection(urlparts[1])
	else:
		h = HTTPConnection(urlparts[1])

	if method == "GET":
		q = urlparts[2] + '?' + urllib.parse.urlencode(data)
		h.request(method, q, headers=headers)
	else:
		q = urlparts[2]
		h.request(method, q, body=urllib.parse.urlencode(data), headers=headers)

	return h.getresponse()
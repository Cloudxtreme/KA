#gideon (WIP)

gideon is a virtual assistant written in python who can be taught commands easily. It is meant to be easy to write plugins for. I (and @argentum47) are new to python and are exploring the language as we write this.

###Present state:

- the google command works (I think)
- empty command returns some random message
- some basic command processing structure works
- GTK-CSS is next

###Plugins

Plugins are dynamically loaded on command processing, and must be registered first. The `process` command from the loaded module is called with the first argument as the raw command from input, and the rest of the commands are the `dictresult` of executing the regex (on the command) passed at plugin registration.

The process must return a dict itself containing the `description` key with markup to show to the user, and optionally a `heading`, and `image` url, and an `link` as a "Read more at..." link to display.

###Todo

- Maintain session history
- GTK-CSS (cc @argentum47)
- make more plugins work
	- the define plugin using the (terrible) wiktionary api needs a parser to work
	- urban
	- nudge (no idea how to implement)
	- learn (and forget)
	- etc. etc.
- use it

###Stuff

This was just a random thought which came to me. And I wanted to use Python on something (had heard lots of good stuff about it, all rightly so). The high-level user API and commands are inspired from Zirak's SO Chatbot

good night

 - awalGarg
 - argentum47 (writing it on your behalf :P)

###License

I unno. WTFPL maybe? @argentum47 decide between WTFPL and MIT please?

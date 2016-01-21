# NOTE: This is under a complete rewrite. The code here was written a loooong time ago, and I wanted it to "just work". It probably doesn't even work now.

#KA (WIP)

KA is a virtual assistant written in Python who can be taught commands easily. More complex commands in the form of plugins can also be written.

###Present state

Pre-alpha stage. Some commands like `google`, `define`, `should I do this... or that`, `urban foo bar` etc. work. Need to write more plugins, and improve overall app structure. Some UI improvement too.

To use, run the `start` file in the root folder. Installing the `Lato` font will make it look more pretty. Requires Python 3.4 and GTK 3.10 to work (most recent distros will work out of the box, like Ubuntu 14.04 etc.).

Windows and MacOSX are not supported. You're welcome :)

###Plugins

Plugins are dynamically loaded on command processing, and must be registered first. The `process` command from the loaded module is called with the first argument as the raw command from input, and the rest of the commands are the `dictresult` of executing a regex (on the command) passed at plugin registration.

The return value of the function must be a `GtkWidget` or one of it's descendant (most likely `GtkGrid`) which will be appended to the content `GtkViewport`.

###Todo

- autostart
- app indicator
- make more plugins 
	- remind (no idea how to implement)
	- learn (and forget)
	- tweet?
	- email updates?
	- etc. etc.
	- listcommands, clear history, etc.
- use it

###Stuff

This was just a random thought which came to me. And I wanted to use Python on something (had heard lots of good stuff about it, all rightly so). The high-level user API and commands are inspired from Zirak's SO Chatbot at https://github.com/Zirak/SO-Chatbot.

License - MIT

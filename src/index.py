from gi.repository import Gtk, Gdk, GdkPixbuf
from pprint import pprint
from routeCmd import fetchResponse
import urllib

ENTER_KEY = 65288

class GideonUI(Gtk.Window):
	def __init__(self, gladeFile = './xml/gideon_layout.glade'):

		self.gladeFile = gladeFile
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.gladeFile)
		self.builder.connect_signals(Handlers)
		self.window = self.builder.get_object("Window")
		self.window.show_all()
		self.el("processing").hide()
		self.el("heading").hide()
		self.el("image").hide()
		self.el("description").hide()
		self.el("outlink").hide()

	def el(self, id):
		return self.builder.get_object(id)

	def main(self):
		print("3... 2... 1... We have ignition!")
		Gtk.main()

	def pushResponse(self, heading = None, image = None, description = '', link = None):
		if not heading:
			UI.el("heading").hide()
		else:
			UI.el("heading").set_markup(heading)
			UI.el("heading").show()
		if not image:
			UI.el("image").hide()
		else:
			imageData = urllib.urlopen(image)
			loader = GdkPixbuf.PixbufLoader()
			loader.write(imageData.read())
			loader.close()
			UI.el("image").set_from_pixbuf(loader.get_pixbuf())
			UI.el("image").show()
		UI.el("description").set_markup(description)
		UI.el("description").show()
		if not link:
			UI.el("outlink").hide()
		else:
			UI.el("outlink").set_uri(link)
			UI.el("outlink").set_label("Read more at " + urllib.urlparse(link)[1])
			UI.el("outlink").show()
		UI.el("processing").stop()
		UI.el("processing").hide()


class Handlers:
	def exit(self, *args):
		print("oi, bye!")
		Gtk.main_quit()

	def processCmd(self):
		print("processing a command!")
		UI.el("processing").show()
		UI.el("processing").start()
		response = fetchResponse(UI.el("cmd").get_text())
		UI.pushResponse(**response)

UI = GideonUI()
UI.main()
from gi.repository import Gtk, Gdk, GObject, GLib
import app

class ResponseWrap:
	def __init__(self, gladeFile = './ui/response/simple.xml'):
		self.gladeFile = gladeFile
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.gladeFile)
		if self.el("username"):
			self.el("username").set_text(app.botname)

	def el(self, id):
		return self.builder.get_object(id)
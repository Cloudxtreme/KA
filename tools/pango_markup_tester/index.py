from gi.repository import Gtk, Gdk, GLib

class Handlers:
	def keypress(self, *args):
		try:
			startiter, enditer = UI.buffer.get_bounds()
			text = UI.buffer.get_text(startiter, enditer, False)
			UI.el("escaped").set_text(GLib.markup_escape_text(text))
			UI.el("pango").set_markup(text)
		except Exception as e:
			UI.el("console").set_text(str(e))
	def delete(self, *args):
		Gtk.main_quit()

class PangoUI(Gtk.Window):
	def __init__(self, gladeFile = './layout.xml'):
		Gtk.Window.__init__(self, title='Pango Markup Tester | Gideon Tools')
		self.gladeFile = gladeFile
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.gladeFile)
		self.builder.connect_signals(Handlers)
		self.window = self.builder.get_object("Window")
		self.buffer = self.el("inputbuffer")
		self.window.show_all()

	def el(self, id):
		return self.builder.get_object(id)

	def main(self):
		Gtk.main()

UI = PangoUI()
UI.main()

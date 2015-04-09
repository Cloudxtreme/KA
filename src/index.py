import app
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
from utils import route_cmd
from urllib.request import urlopen

class AppUI(Gtk.Window):
	def __init__(self, gladeFile = './ui/layout.xml'):
		Gtk.Window.__init__(self, title=app.name)
		self.gladeFile = gladeFile
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.gladeFile)
		self.builder.connect_signals(Handlers)
		self.initCSS()
		self.window = self.el("window")
		window_hints = Gdk.WindowHints(6)
		window_geometry = Gdk.Geometry()
		window_geometry.min_height = 600
		window_geometry.max_height = 720
		window_geometry.min_width = 320
		window_geometry.max_width = 320
		self.window.set_geometry_hints(self.window, window_geometry, window_hints)
		self.window.show_all()

	def initCSS(self, cssFile = './css/layout.css'):
		self.style_provider = Gtk.CssProvider()
		self.cssFile = cssFile;
		self.style_provider.load_from_path(cssFile)
		Gtk.StyleContext.add_provider_for_screen(
			Gdk.Screen.get_default(),
			self.style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		)

	def el(self, id):
		return self.builder.get_object(id)

	def main(self):
		app.logger.info("3... 2... 1... We have ignition!")
		Gtk.main()

	def pushResponse(self, message, props = 'foo'):
		self.el("contentbox").add(message)
		self.el("contentbox").show_all()
		self.el("process").stop()
		app.logger.info(["command successfully processed", props])


class Handlers:
	def delete(self, *args):
		app.logger.info("We are back to Earth. Signing off!")
		Gtk.main_quit()

	def activate(self):
		if (UI.el("cmd").get_text()=="!!reload"):
			return UI.style_provider.load_from_path(UI.cssFile)
		if (UI.el("cmd").get_text().startswith('>>>')):
			return print(eval(UI.el("cmd").get_text().lstrip('>')))
		app.logger.info("processing a command!")
		UI.el("process").start()
		response = route_cmd.process(UI.el("cmd").get_text())
		UI.pushResponse(response)

UI = AppUI()
UI.main()
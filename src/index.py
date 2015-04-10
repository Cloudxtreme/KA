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
		self.el("process").set_opacity(0)

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

	def add_self_command(self, cmd):
		if (cmd == ''):
			return
		lab = Gtk.Label(cmd)
		lab.get_style_context().add_class("user-entered-cmd")
		lab.set_line_wrap(True)
		lab.set_alignment(0, 0)
		self.el("contentbox").add(lab)
		lab.set_visible(True)

	def scroll_to_bottom(self):
		vadjustment = UI.el("contentscroller").get_vadjustment()
		vadjustment.set_value(vadjustment.get_upper())

	def pushResponse(self, message, props = 'foo'):
		self.el("contentbox").add(message)
		self.el("contentbox").show_all()
		UI.el("process").set_opacity(0)
		app.logger.info(["command successfully processed", props])


class Handlers:
	def delete(self, *args):
		app.logger.info("We are back to Earth. Signing off!")
		Gtk.main_quit()

	def activate(self):
		UI.el("process").set_opacity(0.8)
		cmd = UI.el("cmd").get_text()
		UI.add_self_command(cmd)
		if (cmd=="!!reload"):
			UI.el("process").set_opacity(0)
			return UI.style_provider.load_from_path(UI.cssFile)
		if (cmd.startswith('>>>')):
			UI.el("process").set_opacity(0)
			return print(eval(cmd.lstrip('>')))
		app.logger.info("processing a command!")
		response = route_cmd.process(cmd)
		UI.pushResponse(response)
		UI.scroll_to_bottom()

UI = AppUI()
UI.add_self_command("Welcome!")
UI.main()
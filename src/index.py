import app
import os
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
from gi.repository import AppIndicator3 as appindicator
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
		self.positionWindow()
		self.window.show_all()
		self.el("process").set_opacity(0)

	def positionWindow(self):
		window_hints = Gdk.WindowHints(6)
		window_geometry = Gdk.Geometry()
		window_geometry.min_height = 600
		window_geometry.max_height = 720
		window_geometry.min_width = 320
		window_geometry.max_width = 320
		self.window.set_geometry_hints(self.window, window_geometry, window_hints)
		width, _ = self.window.get_size()
		self.window.move(Gdk.Screen.get_default().get_width() - width, 0)
		self.window.set_keep_above(True)
		self.window.stick()

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
		if (cmd == ''): return
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

	def createIndicator(self):
		icon_image = os.path.abspath('./res/app_icon.ico')
		self.ind = appindicator.Indicator.new(app.name, icon_image, appindicator.IndicatorCategory.APPLICATION_STATUS)
		self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
		self.ind.set_label(app.name, "100%")
		menu = Gtk.Menu()
		show_button = Gtk.MenuItem("Show")
		hide_button = Gtk.MenuItem("Hide")
		exit_button = Gtk.MenuItem("Exit")
		menu.attach(show_button, 0, 1, 0, 1)
		menu.attach(hide_button, 0, 1, 0, 1)
		menu.attach(exit_button, 0, 1, 0, 1)
		menu.show_all()
		show_button.connect("activate", Handlers.showwindow)
		hide_button.connect("activate", Handlers.hidewindow)
		exit_button.connect("activate", Handlers.delete)
		self.ind.set_menu(menu)


class Handlers:
	def delete(self = None, *args):
		app.logger.info("We are back to Earth. Signing off!")
		Gtk.main_quit()

	def hidewindow(*_):
		UI.el("window").hide()

	def showwindow(*_):
		UI.el("window").show()
		UI.el("window").set_keep_above(True)
		UI.el("window").stick()

	def activate(self):
		cmd = UI.el("cmd").get_text().strip()
		if not cmd: return
		UI.el("process").set_opacity(0.8)
		UI.add_self_command(cmd)
		app.logger.info("processing a command!")
		response = route_cmd.process(cmd, UI)
		UI.pushResponse(response)
		UI.window.show_all()
		UI.scroll_to_bottom()

	def indicator_scroll(indicator, steps, direction):
		if direction == Gdk.ScrollDirection.UP:
			UI.window.hide()
		elif direction == Gdk.ScrollDirection.DOWN:
			UI.window.show()
			UI.window.present()
		else:
			return

UI = AppUI()
UI.add_self_command("Welcome!")
UI.createIndicator()
UI.main()
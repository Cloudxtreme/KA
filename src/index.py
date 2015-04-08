from gi.repository import Gtk, Gdk, GdkPixbuf
from pprint import pprint
from routeCmd import fetchResponse
from urllib.request import urlopen

class GideonUI(Gtk.Window):
	def __init__(self, gladeFile = './xml/chat_style_layout.glade'):
		Gtk.Window.__init__(self, title='foo')
		self.gladeFile = gladeFile
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.gladeFile)
		self.builder.connect_signals(Handlers)
		self.initCSS()
		self.window = self.builder.get_object("window")
		self.window.show_all()
		self.el("process").hide()
		# self.el("heading").hide()
		# self.el("image").hide()
		# self.el("description").hide()
		# self.el("outlink").hide()

	def initCSS(self, cssFile = './css/chat_style_layout.css'):
		# self.el("cmdboxwrapper").style.
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
		print("3... 2... 1... We have ignition!")
		Gtk.main()

	def pushResponse(self, heading = None, image = None, description = '', link = None):
		return print("push response disabled!")
		if not heading:
			UI.el("heading").hide()
		else:
			UI.el("heading").set_markup(heading)
			UI.el("heading").show()
		if not image:
			UI.el("image").hide()
		else:
			imageData = urlopen(image)
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
	def ondelete(self, *args):
		print("oi, bye!")
		Gtk.main_quit()

	def onactivate(self):
		if (UI.el("cmd").get_text()=="reload"):
			return UI.style_provider.load_from_path(UI.cssFile)
		if (UI.el("cmd").get_text().startswith('>>')):
			return print(eval(UI.el("cmd").get_text().lstrip('>')))
		print("processing a command!")
		UI.el("process").show()
		UI.el("process").start()
		response = fetchResponse(UI.el("cmd").get_text())
		UI.pushResponse(**response)

UI = GideonUI()
UI.main()
from gi.repository import Gtk, Gdk

class GideonUI(Gtk.Window):
    def on_window1_destroy(self, *args):
        Gtk.main_quit()

    def on_gtk_quit_activate(self, *args):
        Gtk.main_quit()

    def on_text_entry_activate(self, *args):
        self.text = self.builder.get_object('text_entry')
        self.chats = self.builder.get_object('chat_window')

        self.chats.set_text(self.chats.get_text() + "\n" + self.text.get_text())

    def __init__(self):
        self.gladefile = '../xml/ui.glade'
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object('window1')
        self.window.show_all()

main = GideonUI()
Gtk.main()

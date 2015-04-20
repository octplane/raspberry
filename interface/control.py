#!/usr/bin/env python

# example helloworld.py

import pygtk
pygtk.require('2.0')
import gtk
from phue import Bridge


class GroupButton(gtk.Button):
    def __init__(self):
        gtk.Button.__init__(self, stock= gtk.STOCK_OK)
        self.set_use_stock(True)

    def set_group_id(self, br,  l):
        self.br = br
        self.group_id = l
        self.updateLabel()

    def state(self):
        return all(map(lambda l: self.br.get_light(int(l), 'on') , self.br.get_group(self.group_id, 'lights')))

    def updateLabel(self):
        if self.state():
            self.set_label("Off " + self.br.get_group(self.group_id, 'name'))
        else:
            self.set_label("On " + self.br.get_group(self.group_id, 'name'))

    def toggle(self):
        print self.state()
        if self.state():
            self.br.set_group(self.group_id, 'on', False)
        else:
            self.br.set_group(self.group_id, 'on', True)
        self.updateLabel()


class LightButton(gtk.Button):
    def __init__(self):
        gtk.Button.__init__(self, gtk.STOCK_OK)

    def set_light(self, l):
        self.light = l
        self.updateLabel()

    def updateLabel(self):
        if self.light.on:
            self.set_label("Off " + self.light.name)
        else:
            self.set_label("On " + self.light.name)

    def toggle(self):
        if self.light.on:
            self.light.on = False
        else:
            self.light.on = True
        self.updateLabel()



class HelloWorld:

    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    def hello(self, widget, data=None):
        self._bridge.set_light( 1, 'on', True)

    def click(self, widget, light=None):
        light.toggle()


    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"

        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # self.window.set_decorated(False)

        # When the window is given the "delete_event" signal (this is given
        # by the window manager, usually by the "close" option, or on the
        # titlebar), we ask it to call the delete_event () function
        # as defined above. The data passed to the callback
        # function is NULL and is ignored in the callback function.
        self.window.connect("delete_event", self.delete_event)

        # Here we connect the "destroy" event to a signal handler.
        # This event occurs when we call gtk_widget_destroy() on the window,
        # or if we return FALSE in the "delete_event" callback.
        self.window.connect("destroy", self.destroy)
        # Sets the border width of the window.
        self.window.set_border_width(0)


        self._bridge = Bridge(ip = '192.168.0.18', username = "149171db2cd4b12f26cc0ce3336b36b7")
        self._lights = self._bridge.lights

        bix = gtk.HBox(homogeneous=True, spacing=0)
        box = gtk.VBox(spacing=0)



        bix.pack_start(box, True, True, 0)

        self.buttons = []
        for light in  self._bridge.lights:

            but = LightButton()
            but.set_light(light)
            self.buttons.append(but)
            but.connect("clicked", self.click, but)
            box.pack_start(but, True, True, 0)
            but.show()

        bux = gtk.VBox(spacing=0)

        for group in self._bridge.groups:
            but = GroupButton()
            but.set_group_id(self._bridge, group.group_id)
            but.connect("clicked", self.click, but)
            bux.pack_start(but, True, True, 0)
            but.show()

        bix.pack_start(bux, True, True, 0)

        exit_button = gtk.Button("Quit", gtk.STOCK_QUIT)
        exit_button.connect("clicked", self.destroy)
        exit_button.show()

        bux.pack_start(exit_button)
        # and the window
        self.window.add(bix)
        map(lambda l: l.show(), (bix, bux, box))

        self.window.show()
        self.window.set_default_size(320, 240)
        # self.window.fullscreen()


    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
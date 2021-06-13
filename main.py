import sys
import time

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from mpris2 import Player
from pypresence import Presence

DBusGMainLoop(set_as_default=True)

RPC = Presence(sys.argv[1])  # Initialize the client class
RPC.connect()  # Start the handshake loop

c_artists = ""
c_title = ""
status = 0


def set_paused():
    global status
    status = 1
    RPC.update(state="En pause", large_image="musicicon")


def set_stopped():
    global status
    status = 0
    RPC.update(state="Aucune musique en cours", large_image="musicicon")


player = None
while player is None:
    try:
        print("Trying to connect.....")
        player = Player(dbus_interface_info={'dbus_uri': 'org.mpris.MediaPlayer2.tdesktop'})
        if player.PlaybackStatus == 'Paused':
            set_paused()
        else:
            a = player.Metadata
            c_title = a["xesam:title"]
            c_artists = a["xesam:artist"]
            RPC.update(state=c_title, details=c_artists, large_image="musicicon")
        print("Connected")
    except:
        time.sleep(5)


def get_info(self, *args, **kw):
    global c_title
    global c_artists
    global status
    try:
        if args[0]["PlaybackStatus"] == 'Stopped':
            set_stopped()
        elif args[0]["PlaybackStatus"] == 'Paused':
            set_paused()
        elif args[0]["PlaybackStatus"] == 'Playing':
            status = 2
            RPC.update(state=c_title, details=c_artists, large_image="musicicon")
    except KeyError:
        try:
            c_title = args[0]["Metadata"]["xesam:title"]
            c_artists = args[0]["Metadata"]["xesam:artist"]
            RPC.update(state=c_title, details=c_artists, large_image="musicicon")
        except KeyError:
            pass
        pass


player.PropertiesChanged = get_info

mloop = GLib.MainLoop()
mloop.run()

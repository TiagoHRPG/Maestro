import dbus
import time

class Controller:
    def __init__(self):
        bus = dbus.SessionBus()
        spotify = bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")

        # Interface do reprodutor de música MPRIS
        self.iface = dbus.Interface(spotify, "org.mpris.MediaPlayer2.Player")

        self.last_command_time = 0
        self.sleep_time = 0.5

    def check_command_time(self):
        if (time.time() - self.last_command_time) > self.sleep_time:
                self.last_command_time = time.time()
                return True
        return False

    def play(self):
        if self.check_command_time():
            self.iface.Play()
            return True
        return False
    
    def pause(self):
        if self.check_command_time():
            self.iface.Pause()
            return True
        return False

    def next(self):
        if self.check_command_time():
            self.iface.Next()
            return True
        return False
    
    def previous(self):
        if self.check_command_time():
            self.iface.Previous()
            return True
        return False

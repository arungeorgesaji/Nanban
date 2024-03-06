import pulsectl
import threading
import time

class VolumeControl(threading.Thread):
    def __init__(self, button):
        super().__init__()
        self.pulse = pulsectl.Pulse('volume-control')
        self.button = button
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            if self.button.is_pressed:
                self.set_volume(1.0)
            else:
                self.set_volume(0.0)
            time.sleep(1)  # Adjust as needed

    def stop(self):
        self._stop_event.set()

    def set_volume(self, volume):
        sinks = self.pulse.sink_list()
        for sink in sinks:
            self.pulse.volume_set_all_chans(sink, volume)

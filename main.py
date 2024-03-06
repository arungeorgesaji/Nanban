from main_mode import *
from voice_assistant import *
from pulse import *
import threading
import time
import subprocess
from gpiozero import Button
import warnings 
import pulsectl

warnings.simplefilter('ignore')
button1 = Button(2)
button2 = Button(3)

volume_control = VolumeControl(button2)
volume_control.start()  

while True:
    if button1.is_pressed:
        scan_mode()
    else:
        voice_mode()

volume_control.stop()
volume_control.join()


import os
import threading

### === Failsafe Exit === ###
def force_exit():
    print("Exiting due to timeout...")
    os._exit(1)

def set_failsafe(timeout=10):
    timer = threading.Timer(timeout, force_exit)
    timer.start()

import time
import math
from pynput import mouse

class MouseTracker:
    def __init__(self):
        self.distance = 0.0
        self.last_pos = None
        self.start_time = time.time()
        self.listener = None
        self.running = False

    def on_move(self, x, y):
        if self.last_pos is not None:
            dx = x - self.last_pos[0]
            dy = y - self.last_pos[1]
            self.distance += math.hypot(dx, dy)
        self.last_pos = (x, y)

    def start(self):
        self.distance = 0.0
        self.last_pos = None
        self.start_time = time.time()
        self.running = True
        self.listener = mouse.Listener(on_move=self.on_move)
        self.listener.start()

    def get_metrics(self):
        """
        Returns mouse speed (pixels moved per second).
        Calculates over the duration since the last call or start.
        """
        if not self.running:
            return 0.0

        elapsed_time = time.time() - self.start_time
        
        # Calculate mouse speed (pixels per second)
        mouse_speed = self.distance / elapsed_time if elapsed_time > 0 else 0.0

        # Reset counters for the next window
        self.distance = 0.0
        self.start_time = time.time()
        # Keep last_pos to smoothly continue calculating distance

        return mouse_speed

    def stop(self):
        self.running = False
        if self.listener is not None:
            self.listener.stop()
            self.listener = None

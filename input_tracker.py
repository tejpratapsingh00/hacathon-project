import time
from pynput import keyboard

class InputTracker:
    def __init__(self):
        self.total_keys = 0
        self.backspaces = 0
        self.start_time = time.time()
        self.listener = None
        self.running = False

    def on_press(self, key):
        self.total_keys += 1
        if key == keyboard.Key.backspace:
            self.backspaces += 1

    def start(self):
        self.total_keys = 0
        self.backspaces = 0
        self.start_time = time.time()
        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def get_metrics(self):
        """
        Returns typing speed (keys per second) and error rate.
        Calculates over the duration since the last call or start.
        """
        if not self.running:
            return 0.0, 0.0

        elapsed_time = time.time() - self.start_time
        
        # Calculate typing speed (keys per second)
        typing_speed = self.total_keys / elapsed_time if elapsed_time > 0 else 0.0
        
        # Calculate error rate
        error_rate = self.backspaces / self.total_keys if self.total_keys > 0 else 0.0

        # Reset counters for the next window
        self.total_keys = 0
        self.backspaces = 0
        self.start_time = time.time()

        return typing_speed, error_rate

    def stop(self):
        self.running = False
        if self.listener is not None:
            self.listener.stop()
            self.listener = None

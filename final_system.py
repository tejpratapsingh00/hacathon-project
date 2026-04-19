import time
import joblib
import pandas as pd
import warnings
from input_tracker import InputTracker
from mouse_tracker import MouseTracker
from camera_module import CameraModule

try:
    from plyer import notification
except ImportError:
    notification = None

import collections

# Ignore Scikit-learn feature name warnings
warnings.filterwarnings("ignore", category=UserWarning)

class RealTimeSystem:
    def __init__(self, model_path='cognitive_load_model.pkl', window_size=3):
        self.window_size = window_size
        self.is_running = False
        
        self.input_tracker = InputTracker()
        self.mouse_tracker = MouseTracker()
        self.camera_module = CameraModule(camera_index=0)
        
        try:
            self.model = joblib.load(model_path)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

        self.history_size = int(60 / self.window_size)
        self.history = collections.deque(maxlen=self.history_size)
        for _ in range(self.history_size):
            self.history.append({'typing': 0.0, 'mouse': 0.0, 'error': 0.0, 'blink': 0.0})
            
        self.last_notification_time = time.time()

        self.latest_result = {
            "prediction": "Unknown",
            "typing_speed": 0.0,
            "mouse_speed": 0.0,
            "error_rate": 0.0,
            "blink_rate": 0.0
        }

    def start(self):
        print("Starting Real-Time Cognitive Load Detection...")
        self.input_tracker.start()
        self.mouse_tracker.start()
        self.camera_module.start()
        self.is_running = True

    def update(self):
        if not self.is_running:
            return

        typing_speed, error_rate = self.input_tracker.get_metrics()
        mouse_speed = self.mouse_tracker.get_metrics()
        blink_rate = self.camera_module.get_metrics()

        self.history.append({
            'typing': typing_speed,
            'mouse': mouse_speed,
            'error': error_rate,
            'blink': blink_rate
        })

        avg_typing = sum(x['typing'] for x in self.history) / len(self.history)
        avg_mouse = sum(x['mouse'] for x in self.history) / len(self.history)
        avg_error = sum(x['error'] for x in self.history) / len(self.history)
        avg_blink = sum(x['blink'] for x in self.history) / len(self.history)

        if self.model:
            features = pd.DataFrame([[avg_typing, avg_mouse, avg_error, avg_blink]],
                                    columns=['TypingSpeed', 'MouseSpeed', 'ErrorRate', 'BlinkRate'])
            prediction = self.model.predict(features)[0]
        else:
            prediction = "Unknown"

        self.latest_result = {
            "prediction": prediction,
            "typing_speed": avg_typing,
            "mouse_speed": avg_mouse,
            "error_rate": avg_error,
            "blink_rate": avg_blink
        }

        print(f"[{prediction}] Typ: {avg_typing:.1f} | Mous: {avg_mouse:.1f} | Err: {avg_error:.2f} | Blnk: {avg_blink:.1f}")

        # Send Windows notification every 60 seconds
        current_time = time.time()
        if current_time - self.last_notification_time >= 60:
            self.last_notification_time = current_time
            if notification:
                try:
                    msg = f"Typ: {avg_typing:.1f} | Mous: {avg_mouse:.1f} | Err: {avg_error:.2f} | Blnk: {avg_blink:.1f}"
                    notification.notify(
                        title=f"Cognitive Load: {prediction}",
                        message=msg,
                        app_name="Cognitive AI",
                        timeout=5
                    )
                except Exception as e:
                    print(f"Notification error: {e}")

        return self.latest_result

    def stop(self):
        print("Stopping hardware trackers...")
        self.is_running = False
        self.input_tracker.stop()
        self.mouse_tracker.stop()
        self.camera_module.stop()

if __name__ == "__main__":
    system = RealTimeSystem(window_size=3)
    system.start()
    try:
        while True:
            time.sleep(3)
            system.update()
    except KeyboardInterrupt:
        pass
    finally:
        system.stop()

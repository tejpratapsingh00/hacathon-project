import cv2
import threading
import time

class CameraModule:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.running = False
        self.thread = None
        
        # We will use OpenCV's built-in HAAR cascade for eye detection
        # To simulate blink rate, we check how frequently eyes are detected
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        self.blinks = 0
        self.start_time = time.time()
        self.eyes_previously_detected = True

    def start(self):
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        self.running = True
        self.blinks = 0
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while self.running:
            if not self.cap.isOpened():
                break
                
            ret, frame = self.cap.read()
            if not ret:
                continue
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eyes = self.eye_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Simple heuristic: if eyes were detected previously but not now, it's a blink
            eyes_detected = len(eyes) > 0
            
            if self.eyes_previously_detected and not eyes_detected:
                self.blinks += 1
                
            self.eyes_previously_detected = eyes_detected
            
            time.sleep(0.1) # Check 10 times a second

    def get_metrics(self):
        """
        Returns blink rate (blinks per minute) for the recent window.
        """
        if not self.running:
            return 0.0

        elapsed_time = time.time() - self.start_time
        blink_rate = (self.blinks / elapsed_time) * 60 if elapsed_time > 0 else 0.0

        # Reset counter for the next window
        self.blinks = 0
        self.start_time = time.time()

        return float(blink_rate)

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()
        if self.cap is not None:
            self.cap.release()

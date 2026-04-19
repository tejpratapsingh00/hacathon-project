import time
import pandas as pd
import os
from input_tracker import InputTracker
from mouse_tracker import MouseTracker
from camera_module import CameraModule

def collect_data(duration_seconds=30, window_size=2, output_file='dataset.csv'):
    print(f"Starting Data Collection for {duration_seconds} seconds...")
    print("Please type, move your mouse, and simulate different workload behaviors.")
    
    input_tracker = InputTracker()
    mouse_tracker = MouseTracker()
    camera_tracker = CameraModule()
    
    input_tracker.start()
    mouse_tracker.start()
    camera_tracker.start()
    
    data = []
    
    try:
        # Collect data in chunks of `window_size` seconds
        iterations = int(duration_seconds / window_size)
        for i in range(iterations):
            time.sleep(window_size)
            
            typing_speed, error_rate = input_tracker.get_metrics()
            mouse_speed = mouse_tracker.get_metrics()
            blink_rate = camera_tracker.get_metrics()
            
            # Logic: HIGH if typing > 5.0 OR mouse > 180 OR error > 0.04 OR blink > 25
            if typing_speed > 5.0 or mouse_speed > 180 or error_rate > 0.04 or blink_rate > 25:
                label = "High"
            else:
                label = "Low"
            
            print(f"Sample {i+1}/{iterations} | Mouse: {mouse_speed:.1f} | Error: {error_rate:.2f} | Blinks: {blink_rate:.1f} | Label: {label}")
            
            data.append({
                'TypingSpeed': typing_speed,
                'MouseSpeed': mouse_speed,
                'ErrorRate': error_rate,
                'BlinkRate': blink_rate,
                'Label': label
            })
            
    except KeyboardInterrupt:
        print("\nData collection interrupted.")
    finally:
        input_tracker.stop()
        mouse_tracker.stop()
        camera_tracker.stop()
        print("Hardware tracking stopped.")
        
    df = pd.DataFrame(data)
    
    # Append to CSV or create new
    if os.path.exists(output_file):
        df.to_csv(output_file, mode='a', header=False, index=False)
    else:
        df.to_csv(output_file, index=False)
        
    print(f"Data saved to {output_file}. Total rows: {len(df)}")

if __name__ == "__main__":
    # Feel free to run this multiple times to gather enough data.
    collect_data(duration_seconds=60, window_size=3)

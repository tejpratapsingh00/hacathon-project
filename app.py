from flask import Flask, render_template, jsonify
import threading
import time
import os
from final_system import RealTimeSystem

app = Flask(__name__)

# Initialize the Real-Time System
system = RealTimeSystem(window_size=3)

def background_tracker():
    system.start()
    try:
        while True:
            time.sleep(3)
            system.update()
    except Exception as e:
        print(f"Error in background tracker: {e}")
    finally:
        system.stop()

# Start background thread
thread = threading.Thread(target=background_tracker, daemon=True)
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    return jsonify(system.latest_result)

if __name__ == "__main__":
    # Ensure templates directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    # Run server
    app.run(debug=False, port=5000)

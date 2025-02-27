import ldclient
from ldclient import Context
from ldclient.config import Config
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import threading
import time
import requests

# Initialize Flask app and WebSocket support
app = Flask(__name__)
app.secret_key = '8e5acb07c20c16c6b410c0d8fd7e71c1'
socketio = SocketIO(app)

# LaunchDarkly setup
LD_SDK_KEY = "sdk-07570192-cfd4-40ff-97ae-ae8a420bc6b8"
FEATURE_FLAG_KEY = "feature_2.0"
LD_API_KEY = "api-02b52e02-600d-4358-a11d-2342855d918d"
PROJECT_KEY = "default"

ldclient.set_config(Config(LD_SDK_KEY))
client = ldclient.get()

if client.is_initialized():
    print("LaunchDarkly client initialized successfully!")
else:
    print("LaunchDarkly client failed to initialize.")

# Function to check feature flag in real-time
def flag_listener():
    context = Context.builder("context-key-123abc").name("Sandy").build()
    current_flag_value = client.variation(FEATURE_FLAG_KEY, context, False)
    while True:
        time.sleep(2)  # Polling interval
        new_flag_value = client.variation(FEATURE_FLAG_KEY, context, False)
        if new_flag_value != current_flag_value:
            print(f"Feature flag changed: {new_flag_value}")
            socketio.emit('flag_update', {'enabled': new_flag_value})
            current_flag_value = new_flag_value

# Start the flag listener in a separate thread
thread = threading.Thread(target=flag_listener, daemon=True)
thread.start()

@app.route('/')
def index():
    return render_template('task1.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    context = Context.builder("context-key-123abc").name("Sandy").build()
    flag_value = client.variation(FEATURE_FLAG_KEY, context, False)
    socketio.emit('flag_update', {'enabled': flag_value})

@app.route('/remediate', methods=['POST'])
def remediate():
    """Disables the feature flag instantly."""
    headers = {
    "Authorization": LD_API_KEY,
    "Content-Type": "application/json"
}

    data = [
        {"op": "replace", "path": f"/environments/launch-darkly-project/on", "value": False}
    ]

    url = f"https://app.launchdarkly.com/api/v2/flags/default/{FEATURE_FLAG_KEY}"

    response = requests.patch(url, headers=headers, json=data)


    if response.status_code == 200:
        print("Feature flag disabled successfully.")
        socketio.emit('flag_update', {'enabled': False})
        return jsonify({"status": "Feature Disabled"}), 200
    else:
        print("Failed to disable feature flag.", response.text)
        return jsonify({"status": "Failed", "error": response.text}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True)

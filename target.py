import ldclient
from ldclient import Context
from ldclient.config import Config
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import threading
import time
import requests
from dotenv import load_dotenv, dotenv_values
import os

# Initialize Flask app and WebSocket support
app = Flask(__name__)
app.secret_key = '8e5acb07c20c16c6b410c0d8fd7e71c1'
socketio = SocketIO(app)
load_dotenv()

# LaunchDarkly promo-banner flag setup
LD_SDK_KEY = os.getenv("LD_SDK_KEY")
FEATURE_FLAG_KEY = os.getenv("FEATURE_FLAG_KEY_1") # launchdarkly:promo-banner
LD_API_KEY = os.getenv("LD_API_KEY")
PROJECT_KEY = os.getenv("PROJECT_KEY")
ENVIRONMENT_KEY = os.getenv("ENVIRONMENT_KEY")

ldclient.set_config(Config(LD_SDK_KEY))
client = ldclient.get()

if client.is_initialized():
    print("LaunchDarkly client initialized successfully!")
else:
    print("LaunchDarkly client failed to initialize.")

def get_context(user_key, role, location, subscription_status,email):
    return Context.builder(user_key) \
        .set("role", role) \
        .set("location", location) \
        .set("subscription_status", subscription_status) \
        .set("email", email)\
        .build()

# Function to check promo-banner flag in real-time
def flag_listener():
    user_context = get_context("Chiarra", "premium_user", "US", "active","chiarra@abc.com")
    current_flag_value = client.variation(FEATURE_FLAG_KEY, user_context, False)
    while True:
        time.sleep(2)  # Polling interval
        new_flag_value = client.variation(FEATURE_FLAG_KEY, user_context, False)
        if new_flag_value != current_flag_value:
            print(f"Feature flag changed: {new_flag_value}")
            socketio.emit('flag_update', {'enabled': new_flag_value})
            current_flag_value = new_flag_value

# Start the promo-banner flag listener in a separate thread
thread = threading.Thread(target=flag_listener, daemon=True)
thread.start()

@app.route('/')
def index():
    return render_template('target.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    user_context = get_context("Chiarra", "premium_user", "US", "active","chiarra@abc.com")
    flag_value = client.variation(FEATURE_FLAG_KEY, user_context, False)
    socketio.emit('flag_update', {'enabled': flag_value})

@app.route('/check_feature/<user_key>/<role>/<location>/<subscription_status>/<email>')
def check_feature(user_key, role, location, subscription_status, email):
    """Checks if the feature is enabled for a specific user."""
    user_context = get_context(user_key, role, location, subscription_status,email)
    print("🔹 Context Sent to LaunchDarkly:", user_context)
    flag_enabled = client.variation(FEATURE_FLAG_KEY, user_context, False)
    print(f"🔹 Feature Flag ({FEATURE_FLAG_KEY}) Status: {flag_enabled}")
    return jsonify({"feature_enabled": flag_enabled})

@app.route('/track_click', methods=['POST'])
def track_click():
    """Tracks when a user clicks the promo banner's CTA button."""
    user_context = get_context("Chiarra", "premium_user", "US", "active", "chiarra@abc.com")
    
    # Send event to LaunchDarkly
    client.track("promo-banner-click", user_context)
    
    print("✅ Click event tracked in LaunchDarkly.")
    return jsonify({"status": "click recorded"})

@app.route('/track_conversion', methods=['POST'])
def track_conversion():
    """Tracks a successful conversion event (e.g., sign-up, purchase)."""
    user_context = get_context("Chiarra", "premium_user", "US", "active", "chiarra@abc.com")
    
    # Send conversion event to LaunchDarkly
    client.track("promo-banner-conversion", user_context)
    
    print("🎯 Conversion event tracked in LaunchDarkly.")
    return jsonify({"status": "conversion recorded"})


@app.route('/remediate_promo', methods=['POST'])
def remediate_promo():
    """Disables the promo-banner feature flag instantly."""
    headers = {
        "Authorization": "LD_API_KEY",
        "Content-Type": "application/json"
    }
    data = [
        {"op": "replace", "path": f"/environments/{ENVIRONMENT_KEY}/on", "value": False}
    ]
    url = f"https://app.launchdarkly.com/api/v2/flags/{PROJECT_KEY}/{FEATURE_FLAG_KEY}"
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print("promo-banner feature flag disabled successfully.")
        socketio.emit('flag_update', {'enabled': False})
        return jsonify({"status": "Feature Disabled"}), 200
    else:
        print("Failed to disable promo-banner feature flag.", response.text)
        return jsonify({"status": "Failed", "error": response.text}), 500

if __name__ == '__main__':
    socketio.run(app, debug=True)

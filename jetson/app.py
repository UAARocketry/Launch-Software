from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import time
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Serve the HTML dashboard
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# Background telemetry generator
def generate_telemetry():
    while True:
        telemetry_data = {
            "lox_pressure": random.randint(350, 400),
            "ipa_pressure": random.randint(300, 350),
            "chamber_pressure": random.randint(250, 300),
            "mixture_ratio": round(random.uniform(2.5, 3.0), 2),
            "lox_temp": random.randint(-183, -180),
            "ipa_temp": random.randint(20, 25),
            "chamber_temp": random.randint(25, 30),
        }
        socketio.emit("telemetry", telemetry_data)
        time.sleep(1)  # Adjust update interval as needed

# Start telemetry in a background thread
thread = Thread(target=generate_telemetry)
thread.daemon = True
thread.start()

# Run the server
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
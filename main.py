from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
import camera

app = Flask(__name__)
socketio = SocketIO(app)

# Shared slider values
data = {'xMin': 10, 'xMax': 314, 'yMin': 10, 'yMax': 233}

@app.route('/')
def index():
    return render_template('index.html')

# MJPEG camera feed
@app.route('/stream')
def stream():
    return Response(camera.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# WebSocket events
@socketio.on('connect')
def on_connect():
    print("someone connecting")
    socketio.emit('state', data)

@socketio.on('update')
def on_update(msg):
    print("update:", msg)
    data.update(msg)
    socketio.emit('state', data)

if __name__ == '__main__':
    print("Hello!")
    socketio.run(app, host='192.168.178.50', port=8080)
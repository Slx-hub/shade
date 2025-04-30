from picamera2 import Picamera2
import cv2, time

def gen_frames():
    picam2 = Picamera2()
    config = picam2.create_video_configuration(
        raw={"size": (2592, 1944)},                          # full-sensor
        main={"size": (324, 243), "format": "RGB888"},       # downscaled
        controls={"FrameRate": 10}
    )
    picam2.configure(config)
    picam2.start()
    time.sleep(1)

    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        ret, buf = cv2.imencode('.jpg', gray)
        if not ret:
            continue
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')

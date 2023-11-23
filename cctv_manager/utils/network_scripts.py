import cv2
import subprocess
import platform
import time


def check_ping(hostname):
    try:
        subprocess.check_output(f'ping -{"n" if platform.system().lower() == "windows" else "c"} 1 {hostname}',
                                shell=True)
    except Exception:
        return False
    return True


def rtsp_connection(hostname, quality):
    if quality not in ['ch00_0', 'ch00_1']:
        raise ValueError('Wrong quality. Should be ch00_1 or ch00_0')

    print(f'Starting for {hostname} with {quality}')
    cap = cv2.VideoCapture(f'rtsp://{hostname}/live/{quality}')

    time.sleep(2)
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f'No frame for {hostname}')
            continue
        ret, encoded_frame = cv2.imencode(".jpg", frame)
        if not ret:
            print(f'No encoded frame for {hostname}')
            continue
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_frame) + b'\r\n'

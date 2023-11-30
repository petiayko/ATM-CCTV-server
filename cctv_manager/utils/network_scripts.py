from pythonping import ping

import cv2
import platform
import subprocess
import time


def check_ping(hostname, count=1):
    return ping(hostname, count=count).success()


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
        ret, encoded_frame = cv2.imencode('.jpg', frame)
        if not ret:
            print(f'No encoded frame for {hostname}')
            continue
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_frame) + b'\r\n'


def get_stream_content(hostname, quality):
    # r = requests.get(f'http://{hostname}/live/{quality}', stream=True)
    #
    # for line in r.iter_lines():
    #     if line:
    #         yield line
    frame = None

    print(f'Starting for {hostname} with {quality}')
    cap = cv2.VideoCapture(f'rtsp://{hostname}/live/{quality}')

    time.sleep(2)
    ret, frame = cap.read()
    if not ret:
        print(f'Cannot read for {hostname}: {ret}')
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        print(f'Cannot imencode for {hostname}: {ret}')
    encoded_frame = buffer.tobytes()
    yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + encoded_frame + b'\r\n'

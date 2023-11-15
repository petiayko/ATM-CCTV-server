import cv2
import ipaddress
import re
import time


def is_ip_valid(ip_addr):
    # checking if the address is valid
    try:
        _ = ipaddress.ip_address(ip_addr)
        return True
    except ValueError:
        return False


def get_video(ip_addr, quality):
    # function for watching video in the window
    # (source: https://stackoverflow.com/questions/17961318/read-frames-from-rtsp-stream-in-python)
    if quality not in ['ch00_0', 'ch00_1']:
        raise ValueError('Wrong quality. Should be ch00_1 or ch00_0')

    if not is_ip_valid(ip_addr):
        raise ValueError('Wrong camera ip address')

    print(f'Starting for {ip_addr} with {quality}')
    cap = cv2.VideoCapture(f'rtsp://{ip_addr}/live/{quality}')

    time.sleep(2)
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('frame', frame)
        else:
            print(f'No video for {ip_addr}')
        if cv2.waitKey(1) and 0xFF == ord('q'):
            print(f'Finishing for {ip_addr}')
            break

    cap.release()
    cv2.destroyAllWindows()


def get_video_for_web(ip_addr, quality):
    # function for encoding video to show it on html page
    # (source: https://pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/)
    if quality not in ['ch00_0', 'ch00_1']:
        raise ValueError('Wrong quality. Should be ch00_1 or ch00_0')

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_addr):
        raise ValueError('Wrong camera ip address')

    print(f'Starting for {ip_addr} with {quality}')
    cap = cv2.VideoCapture(f'rtsp://{ip_addr}/live/{quality}')

    time.sleep(2)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        ret, encoded_frame = cv2.imencode(".jpg", frame)
        if not ret:
            continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encoded_frame) + b'\r\n')

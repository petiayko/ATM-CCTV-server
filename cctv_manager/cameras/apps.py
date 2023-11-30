from django.apps import AppConfig

import cv2
import numpy as np
import datetime
import imutils
import os
import socket
import threading

rtsp_url1 = "cam1"
rtsp_url2 = "cam2"

def cam_recordig(rtsp_url):
    while True:
        try:
            cam = cv2.VideoCapture(rtsp_url)
            avg1 = None
            firstFrame = None
            padding = 20
            # using MPEG, we write almost a MB per second
            maxFileSizeBytes = 10 * 1024 * 1024

            frame_width = int(cam.get(3))
            frame_height = int(cam.get(4))
            fps = int(cam.get(5))
            if fps > 10:
                fps = 5
            fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

            hostname = str(socket.gethostname())

            videoFileF = datetime.datetime.now().strftime("%A %d %B %Y %I-%M-%S%p") + 'framed.avi'
            videoFileR = datetime.datetime.now().strftime("%A %d %B %Y %I-%M-%S%p") + 'raw.avi'
            outF = cv2.VideoWriter(videoFileF ,fourcc, fps, (frame_width,frame_height))
            outR = cv2.VideoWriter(videoFileR ,fourcc, fps, (frame_width,frame_height))

            while True:
                frame = cam.read()[1]
                cv2.rectangle(frame, (0, 0), (500, 50), (0,0,0), -1) # removing the date time from the image
                cv2.rectangle(frame, (0, 0), (frame_width, 375), (0,0,0), -1) # removing trees
                cv2.rectangle(frame, (0, 550), (frame_width, frame_height), (0,0,0), -1) # removing grass
                realFrame = frame.copy()  # we need a copy of the real image that is not modified

                # converting to Greyscale and bluring to factor out small changes
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.GaussianBlur(frame, (21, 21), 0)

                if firstFrame is None:
                    firstFrame = frame
                    avg1 = np.float32(frame)
                    continue

                frameDelta = cv2.absdiff(firstFrame, frame)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

                edges = cv2.Canny(thresh, 30, 150)
                cnts = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]

                output = realFrame.copy()

                if len(cnts) > 0:  # we have movement!
                    boxes = []
                    for c in cnts:
                        (x, y, w, h) = cv2.boundingRect(c)
                        boxes.append([x,y,x+w,y+h])

                    boxes = np.asarray(boxes)
                    # need an extra "min/max" for contours outside the frame
                    left, top, right, bottom = np.min(boxes[:,0]), np.min(boxes[:,1]), np.max(boxes[:,2]), np.max(boxes[:,3])

                    output = realFrame.copy()  #                                                                                               B  G  R
                    cv2.putText(output, hostname + ' ' + datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    cv2.rectangle(output, (left - padding,top - padding), (right + padding,bottom + padding), (0, 255, 0), 2)
                    cv2.imshow("Changes", output)
                    outF.write(output)
                    outR.write(realFrame.copy())

                cv2.putText(realFrame, hostname + ' ' + datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.imshow("realFrame", realFrame)

                key = cv2.waitKey(1)

                if key == 27:
                #    cv2.destroyWindow(winName)
                    quit()

                # updating our firstFrame to average out the background
                cv2.accumulateWeighted(frame,avg1,.3)
                firstFrame = cv2.convertScaleAbs(avg1)  

                if os.stat(videoFileF).st_size >= maxFileSizeBytes:
                    videoFileF = datetime.datetime.now().strftime("%A %d %B %Y %I-%M-%S%p") + 'framed.avi'
                    outF = cv2.VideoWriter(videoFileF ,fourcc, fps, (frame_width,frame_height))
                    videoFileR = datetime.datetime.now().strftime("%A %d %B %Y %I-%M-%S%p") + 'raw.avi'
                    outR = cv2.VideoWriter(videoFileR ,fourcc, fps, (frame_width,frame_height))
            print("Recording stopped")
        except:
            print("Error with camera connection")

th1 = threading.Thread(target=cam_recordig, args=(rtsp_url1,), daemon=True)
th2 = threading.Thread(target=cam_recordig, args=(rtsp_url2,), daemon=True)
th1.start()
th2.start()

class CamerasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cameras'

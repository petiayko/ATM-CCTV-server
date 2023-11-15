from flask import Flask, render_template, Response

from video_handler import get_video_for_web

app = Flask(__name__)


@app.route('/video_stream1')
def video_stream1():
    # handler for url, that provides us with video from the camera (50)
    return Response(get_video_for_web('192.168.0.50', 'ch00_1'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_stream2')
def video_stream2():
    # handler for url, that provides us with video from the camera (51)
    return Response(get_video_for_web('192.168.0.51', 'ch00_1'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def path_root():
    # handler for the only path
    return render_template("index.html")


if __name__ == '__main__':
    # start server
    app.run(port=8000, debug=True)

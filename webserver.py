import cv2, imagezmq, socket
# from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from flask import Flask, render_template, Response

resolved_ip_from_name = socket.gethostbyname('camclient')

app = Flask(__name__)

def sendImagesToWeb():
    # When we have incoming request, create a receiver and subscribe to a publisher
    # NOTE: it seems strange, but we need to specify the IP address of the PUBLISHER
    receiver = imagezmq.ImageHub(open_port=f'tcp://{resolved_ip_from_name}:5566', REQ_REP = False)
    while True:
        # Pull an image from the queue
        camName, frame = receiver.recv_image()
        # Using OpenCV library create a JPEG image from the frame we have received
        jpg = cv2.imencode('.jpg', frame)[1]
        # Convert this JPEG image into a binary string that we can send to the browser via HTTP
        yield b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'+jpg.tobytes()+b'\r\n'


@app.route('/')
def index():
    # return "Hello World"
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(sendImagesToWeb(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # Add `application` method to Request class and define this method here
# @Request.application
# def application(request):
#     # What we do is we `sendImagesToWeb` as Iterator (generator) and create a Response object
#     # based on its output.
#     return Response(sendImagesToWeb(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # This code starts simple HTTP server that listens on interface with IP 192.168.0.114, port 4000
    # run_simple('127.0.0.1', 80, application)
    # run_simple('localhost', 80, application)
    app.run(host='0.0.0.0', port=80, debug=True)
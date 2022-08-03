# code from https://github.com/jeffbass/imagezmq/blob/master/docs/advanced-pub-sub.rst
import imagezmq, socket, cv2

def process_image(image):
    # Do something useful here, for example, run motion detection and record
    # a stream to a file if detected.
    pass

# the hub that receives the incoming images
image_hub = imagezmq.ImageHub(open_port='tcp://localhost:5555', REQ_REP = False)

print(f"HOSTNAME IS {socket.gethostbyname(socket.gethostname())}")

# Create a PUB server to send images for monitoring purposes in a non-blocking mode
stream_monitor = imagezmq.ImageSender(connect_to = 'tcp://127.0.0.1:5566', REQ_REP = False)

while True:  # show streamed images until Ctrl-C
    rpi_name, image = image_hub.recv_image()
    print(rpi_name)
    image_hub.send_reply(b'OK')

    # do any manipulation, inference, etc.
    process_image(image)

    # send the image to the stream monitor
    stream_monitor.send_image(rpi_name, image)

    # if we want to see the images in a window, uncomment the following
    # cv2.imshow(rpi_name, image) # 1 window for each RPi
    # cv2.waitKey(1)

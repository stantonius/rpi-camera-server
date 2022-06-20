from vidgear.gears import NetGear
import cv2

# note: the IP address below is that of the client of the stream, 
# which is actually the home server (the video stream server is the camera)

options = {
    "protocol": "tcp",
    "address": "192.168.0.123",
    "port": "5454",
    "receive_mode": True,
    "logging": True,
    "pattern": 1,
    "flag": 0,
    "copy": False,
    "track": False
}

client = NetGear(**options)

while True:

    # receive frames from network
    frame = client.recv()

    # check for received frame if Nonetype
    if frame is None:
        break

    # {do something with the received frame here}

    # Show output window
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("Output Frame", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# safely close client
client.close()
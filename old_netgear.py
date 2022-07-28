from typing import AsyncGenerator
from vidgear.gears.asyncio import NetGear_Async, WebGear
from vidgear.gears.asyncio.helper import reducer
import os, cv2, asyncio, uvicorn
from dotenv import load_dotenv

load_dotenv()

# note: the IP address below is that of the client of the stream, 
# which is actually the home server (the video stream server is the camera)

options = {
    "protocol": "tcp",
    # "address": os.environ["CLIENT_IP"],
    "address": "0.0.0.0",
    "port": os.environ["CLIENT_PORT"],
    "receive_mode": True,
    "logging": True,
    "pattern": 1,
    "flag": 0,
    "copy": False,
    "track": False
}

webgear_options = {
    "frame_size_reduction": 40,
    "jpeg_compression_quality": 80,
    "jpeg_compression_fastdct": True,
    "jpeg_compression_fastupsample": False,
    "framerate": 60, 
    }

client = NetGear_Async(**options).launch()

async def main():
    async for frame in client.recv_generator():

        # do something with received frame here

        # Show output window (applicable only if not streaming elsewhere)
        # cv2.imshow("Output Frame", frame)
        # key = cv2.waitKey(1) & 0xFF
    
        # reducer frames size if you want more performance otherwise comment this line
        frame = await reducer(
            frame, percentage=30, interpolation=cv2.INTER_AREA
        )  # reduce frame by 30%

        # handle JPEG encoding
        encodedImage = cv2.imencode(".jpg", frame)[1].tobytes()
        # yield frame in byte format
        yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n")
        await asyncio.sleep(0)



if __name__ == "__main__":
    # set event loop to client
    asyncio.set_event_loop(client.loop)
    # initialize WebGear app without any source
    web = WebGear(logging=True, **webgear_options)

    # add your custom frame producer to config with adequate IP address
    web.config["generator"] = main

    # run this app on Uvicorn server at address http://localhost:8000/
    # uvicorn.run(web(), host="127.0.0.1", port=8000)
    uvicorn.run(web(), host="0.0.0.0", port=8000)

    # safely close client
    client.close()

    # close app safely
    web.shutdown()
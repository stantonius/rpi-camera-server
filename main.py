# import libraries
from vidgear.gears.asyncio import NetGear_Async
from vidgear.gears.asyncio import WebGear
from vidgear.gears.asyncio.helper import reducer
import uvicorn, asyncio, cv2

# Define NetGear_Async Client at given IP address and define parameters
# !!! change following IP address '192.168.x.xxx' with yours !!!
client = NetGear_Async(
    address="192.168.0.226",
    port="5454",
    receive_mode=True,
    pattern=1,
    logging=True,
).launch()

# create your own custom frame producer
async def my_frame_producer():

    # loop over Client's Asynchronous Frame Generator
    async for frame in client.recv_generator():

        # {do something with received frames here}

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
    # Set event loop to client's
    asyncio.set_event_loop(client.loop)

    # initialize WebGear app without any source
    web = WebGear(logging=True)

    # add your custom frame producer to config with adequate IP address
    web.config["generator"] = my_frame_producer

    # run this app on Uvicorn server at address http://localhost:8000/
    uvicorn.run(web(), host="localhost", port=8000)

    # safely close client
    client.close()

    # close app safely
    web.shutdown()

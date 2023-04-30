import cv2
import asyncio
import numpy as np
import websockets
from concurrent.futures import ThreadPoolExecutor

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

executor = ThreadPoolExecutor()

async def read_frame():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, cam.read)

async def send_frame(websocket):
    while True:
        ret, frame = await read_frame()
        if ret:
            # Encode the frame to JPEG without reducing quality
            ret, buffer = cv2.imencode('.jpg', frame)
            jpeg_bytes = buffer.tobytes()

            # Send the frame to the server
            await websocket.send(jpeg_bytes)
        else:
            break

async def main():
    async with websockets.connect("ws://192.168.137.1:8888", ping_timeout=None) as websocket:
        await asyncio.wait_for(send_frame(websocket), timeout=60)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

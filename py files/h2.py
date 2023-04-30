import cv2
import asyncio
import numpy as np
import websockets
import imageio_ffmpeg as ffmpeg
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

# Initialize the camera
cam = cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)

executor = ThreadPoolExecutor()

async def read_frame():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, cam.read)

async def send_frame(websocket):
    while True:
        ret, frame = await read_frame()
        if ret:
            # Encode the frame to H.265 format
            ret, buffer = cv2.imencode('.png', frame)
            png_bytes = buffer.tobytes()

            # Convert PNG bytes to H.265 bytes
            input_stream = BytesIO(png_bytes)
            output_stream = BytesIO()
            ffmpeg.write_frames(input_stream, output_stream, fps=30, codec='libx265')

            # Send the frame to the server
            h265_bytes = output_stream.getvalue()
            await websocket.send(h265_bytes)
        else:
            break

async def main():
    async with websockets.connect("ws://192.168.137.1:8888", ping_timeout=None) as websocket:
        await send_frame(websocket)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())


    # Before running the modified code, make sure to install the imageio-ffmpeg library: pip install imageio-ffmpeg


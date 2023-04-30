import cv2
import asyncio
import json
import base64
import numpy as np
import websockets

#initialize the camera
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

async def send_frame(websocket):
    while True:
        ret, frame = cam.read()
        if ret:
            #encode the frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            jpeg_bytes = buffer.tobytes()
            # send the frame to the server
            await websocket.send(jpeg_bytes)
        else:
            break

async def main():
    async with websockets.connect("ws://192.168.137.1:8888", ping_timeout=None) as websocket:
        await send_frame(websocket)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())




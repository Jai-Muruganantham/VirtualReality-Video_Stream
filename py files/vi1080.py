import cv2
import asyncio
import websockets
from concurrent.futures import ThreadPoolExecutor

# Initialize the camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

async def send_frame(websocket):
    while True:
        ret, frame = cam.read()
        if ret:
            # Convert the frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Encode the frame to JPEG with lower quality (e.g., 70)
            ret, buffer = cv2.imencode('.jpg', frame_rgb, [cv2.IMWRITE_JPEG_QUALITY, 70])
            jpeg_bytes = buffer.tobytes()

            # Send the frame to the server
            await websocket.send(jpeg_bytes)
        else:
            break

async def main():
    async with websockets.connect("ws://192.168.137.1:8888", ping_timeout=None) as websocket:
        await send_frame(websocket)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_default_executor(ThreadPoolExecutor())
    loop.run_until_complete(main())

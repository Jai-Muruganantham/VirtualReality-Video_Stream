import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
import asyncio
import websockets

Gst.init(None)

# Set up the GStreamer pipeline
pipeline = Gst.parse_launch("v4l2src ! video/x-raw,width=1280,height=720 ! videoconvert ! jpegenc ! appsink name=mysink")

sink = pipeline.get_by_name("mysink")

async def send_frame(websocket):
    sample = sink.emit("pull-sample")
    if sample:
        buf = sample.get_buffer()
        result, mapinfo = buf.map(Gst.MapFlags.READ)
        if result:
            await websocket.send(mapinfo.data)
            buf.unmap(mapinfo)
        else:
            print("Error: Unable to map buffer")
            sys.exit(1)

async def main():
    pipeline.set_state(Gst.State.PLAYING)
    async with websockets.connect("ws://192.168.137.1:8888") as websocket:
        while True:
            await send_frame(websocket)

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    finally:
        pipeline.set_state(Gst.State.NULL)

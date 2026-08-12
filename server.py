import asyncio
import websockets
import json

class Server:
    def __init__(self):
        print("Starting server...")

# Send data example
#
# async def sendTelemetry(websocket):
#     while True:
#         data = {}
#         await websocket.send(json.dumps(data))
#         await asyncio.sleep(1) # Send every second

# async def main():
#     async with websockets.serve(sendTelemetry, "localhost", 8080):
#         await asyncio.get_running_loop().create_future()

# asyncio.run(main())
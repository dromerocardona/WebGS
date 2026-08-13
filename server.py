import asyncio
import websockets
import json

class Server:
    def __init__(self):
        self.host = "localhost"
        self.port = 8080
        self.clients = set()
        self.server = None
        print("Starting server...")
    
    async def handler(self, websocket):
        """Handle connections"""
        self.clients.add(websocket)
        try:
            async for message in websocket:
                pass
        finally:
            self.clients.discard(websocket)
    
    def send(self, data):
        message = json.dumps(data)
        asyncio.create_task(self.broadcast(message))
    
    async def broadcast(self, message):
        if not self.clients:
            return
        
        dead = set()
        for ws in self.clients:
            try:
                await ws.send(message)
            except (websockets.exceptions.ConnectionClosed):
                dead.add(ws)
        self.clients -= dead
    
    async def start(self):
        self.server = await websockets.serve(self.handler, self.host, self.port)
        await self.server.wait_closed()
    
    def run(self):
        asyncio.run(self.start())



# # EXAMPLE USAGE

# if __name__ == "__main__":
#     server = Server()

#     async def telemetry_loop():
#         while True:
#             data = {
#                 "temperature": 23.5
#             }
#             server.send(data)
#             await asyncio.sleep(1)

#     async def main():
#         asyncio.create_task(telemetry_loop())
#         await server.start()

#     asyncio.run(main())
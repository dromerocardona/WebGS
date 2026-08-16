import asyncio
import websockets
import json
import threading

class Server:
    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port

        self.clients = set()

        self.loop = None
        self.server = None
        self.thread = None

        self.started = threading.Event()
        self.stopped = threading.Event()

        print("Starting server...")

    async def handler(self, websocket):
        """Handle a WebSocket client connection"""
        self.clients.add(websocket)

        try:
            # Keep the connection alive and receive messages (in the future maybe)
            async for message in websocket:
                pass

        except websockets.exceptions.ConnectionClosed:
            pass

        finally:
            self.clients.discard(websocket)

    async def startServer(self):
        """Start the WebSocket server on the server's asyncio loop"""
        self.server = await websockets.serve(
            self.handler,
            self.host,
            self.port
        )

        print(f"WebSocket server started on ws://{self.host}:{self.port}")

        self.started.set()

        try:
            await self.server.wait_closed()
        finally:
            self.stopped.set()

    def start(self):
        """Start the WebSocket server in its own thread."""
        if self.thread is not None and self.thread.is_alive():
            return

        self.started.clear()
        self.stopped.clear()

        self.thread = threading.Thread(
            target=self.run,
            name="WebSocketServer",
            daemon=True
        )

        self.thread.start()

        # Wait until the server is running
        self.started.wait()

    def run(self):
        """Run the server's asyncio event loop"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        try:
            self.loop.run_until_complete(self.startServer())
        finally:
            self.loop.close()
            self.loop = None

    def send(self, data):
        """Send a packet to all connected WebSocket clients"""
        if self.loop is None or not self.loop.is_running():
            return False

        message = json.dumps(data)

        future = asyncio.run_coroutine_threadsafe(
            self.broadcast(message),
            self.loop
        )

        # Don't block the calling thread waiting for the clients
        future.add_done_callback(self.broadcastDone)

        return True

    def broadcastDone(self, future):
        """Handle errors from an asynchronous broadcast"""
        try:
            future.result()
        except Exception as e:
            print(f"Broadcast error: {e}")

    async def broadcast(self, message):
        """Send a message to all connected clients"""
        if not self.clients:
            return

        dead = set()

        for websocket in list(self.clients):
            try:
                await websocket.send(message)

            except websockets.exceptions.ConnectionClosed:
                dead.add(websocket)

            except Exception as e:
                print(f"Error sending to client: {e}")
                dead.add(websocket)

        self.clients -= dead

    def stop(self):
        """Stop the WebSocket server"""
        if self.loop is None or not self.loop.is_running():
            return

        async def shutdown():
            # Close all connected clients
            clients = list(self.clients)

            for websocket in clients:
                try:
                    await websocket.close()
                except Exception:
                    pass

            self.clients.clear()

            # Stop the WebSocket server
            if self.server is not None:
                self.server.close()
                await self.server.wait_closed()

        future = asyncio.run_coroutine_threadsafe(
            shutdown(),
            self.loop
        )

        try:
            future.result(timeout=5)
        except Exception as e:
            print(f"Error stopping server: {e}")

        if self.thread is not None:
            self.thread.join(timeout=5)

        self.thread = None
        self.server = None
        self.loop = None

        print("Server stopped.")


# TESTING

# if __name__ == "__main__":
#     server = Server()

#     try:
#         server.start()

#         while True:
#             packet = {
#                 "test": "test",
#             }

#             print(f"Sending: {packet}")

#             server.send(packet)

#             threading.Event().wait(1)

#     except KeyboardInterrupt:
#         print("\nStopping test server...")

#     finally:
#         server.stop()
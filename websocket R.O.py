import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    global connected_clients
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received data from robot: {message}")
            await websocket.send(f"Server received: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("A robot has disconnected.")
    finally:
        connected_clients.remove(websocket)

start_server = websockets.serve(handler, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
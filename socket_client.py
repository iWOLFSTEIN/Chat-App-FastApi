import socketio
import asyncio

sio = socketio.AsyncClient()


@sio.event
async def connect():
    print("connected")


@sio.on("users")
async def handle_users_event(data):
    print("Received users event:", data)


@sio.event
async def disconnect():
    print("disconnected")


async def main():
    await sio.connect(url="http://127.0.0.1:8000", socketio_path="ws")
    await sio.emit("chats", {"message": "Hello, server!"})
    await sio.wait()
    await sio.disconnect()


asyncio.run(main())

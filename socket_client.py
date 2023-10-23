import socketio
import asyncio

sio = socketio.AsyncClient()
headers = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFiYyIsInBhc3N3b3JkIjoiMTIzNDU2IiwiZXhwIjoxNzAwNDk5MjY1fQ.Y5uv2iOzzZzK35R4qPTFaPRfj1aw3wPCxjkkbkie1ps",
    "user_id": "userid123",
}


@sio.event
async def connect():
    print("connected")


@sio.on("chats")
async def handle_users_chats(data):
    print("Received users chats:", data)


@sio.on("messages")
async def handle_user_messages(data):
    print("Received users messages:", data[0])


@sio.event
async def disconnect():
    print("disconnected")


async def main():
    await sio.connect(url="http://127.0.0.1:8000", socketio_path="ws", headers=headers)
    await sio.emit("get_chats", {"id": "652426912b3e343a0af72bf2"})
    await sio.emit(
        "get_messages",
        {
            "sender_id": "6536b0ab2fa848aa7d4a155c",
            "receiver_id": "652426912b3e343a0af72bf2",
        },
    )
    await sio.wait()
    await sio.disconnect()


asyncio.run(main())

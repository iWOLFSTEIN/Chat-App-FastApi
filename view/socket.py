import socketio

from controller.validate import validate_token
from utils.error_message import ErrorMessage
from utils.exceptions import socket_exception_connection_refused


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
app = socketio.ASGIApp(sio, socketio_path="ws")


@sio.event
async def connect(sid, environ, auth):
    token = environ.get("HTTP_ACCESS_TOKEN")
    if not validate_token(token=token):
        socket_exception_connection_refused(ErrorMessage.invalid_token)
    print("connect ", sid)


@sio.event
async def disconnect(sid):
    print("disconnect ", sid)
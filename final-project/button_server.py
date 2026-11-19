# Read the button, encoder and joystick and send them over WebSocket.
import asyncio
import json
import board
import qwiic_button
import qwiic_joystick
from adafruit_seesaw import seesaw, rotaryio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

button = qwiic_button.QwiicButton(address=0x6F)
if not button.begin():
    raise RuntimeError("Button initialization failed")

device = seesaw.Seesaw(board.I2C(), addr=0x36)
encoder = rotaryio.IncrementalEncoder(device)
start_position = -encoder.position

joystick = qwiic_joystick.QwiicJoystick(address=0x20)
if not joystick.is_connected():
    raise RuntimeError("Joystick not detected")
joystick.begin()


async def send_data(websocket):
    print("Computer connected!", flush=True)
    try:
        while True:
            data = {
                "button": bool(button.is_button_pressed()),
                "encoder": -encoder.position - start_position,
                "joystick": {
                    "x": joystick.get_horizontal(),
                    "y": joystick.get_vertical(),
                    "pressed": joystick.get_button() == 0,
                },
            }
            await websocket.send(json.dumps(data))
            await asyncio.sleep(0.05)
    except ConnectionClosed:
        print("Computer disconnected.", flush=True)


async def main():
    async with serve(send_data, "0.0.0.0", 8765):
        print("Server ready on port 8765", flush=True)
        await asyncio.get_running_loop().create_future()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nServer stopped.")


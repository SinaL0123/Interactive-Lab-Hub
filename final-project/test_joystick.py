# Print joystick horizontal, vertical and push-button readings.
import time
import qwiic_joystick

joystick = qwiic_joystick.QwiicJoystick(address=0x20)
if not joystick.is_connected():
    raise RuntimeError("Joystick not detected")
joystick.begin()
print("Move and press the joystick. Ctrl+C to stop.")

try:
    while True:
        x = joystick.get_horizontal()
        y = joystick.get_vertical()
        pressed = joystick.get_button() == 0
        print(f"X: {x:4d} | Y: {y:4d} | Pressed: {pressed}",
              flush=True)
        time.sleep(0.2)
except KeyboardInterrupt:
    print("\nTest stopped.")


# Print the button state when it changes.
import time
import qwiic_button

button = qwiic_button.QwiicButton(address=0x6F)
if not button.begin():
    raise RuntimeError("Button initialization failed")

print("Ready! Press and release the button. Ctrl+C to stop.")
previous = None
try:
    while True:
        pressed = bool(button.is_button_pressed())
        if pressed != previous:
            print("PRESSED" if pressed else "RELEASED", flush=True)
            previous = pressed
        time.sleep(0.02)
except KeyboardInterrupt:
    print("\nTest stopped.")


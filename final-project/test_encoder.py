# Print the encoder count when it changes.
import time
import board
from adafruit_seesaw import seesaw, rotaryio

device = seesaw.Seesaw(board.I2C(), addr=0x36)
encoder = rotaryio.IncrementalEncoder(device)
start_position = -encoder.position
previous = None

print("Ready! Turn the knob. Ctrl+C to stop.")
try:
    while True:
        position = -encoder.position - start_position
        if position != previous:
            print(f"Position: {position}", flush=True)
            previous = position
        time.sleep(0.02)
except KeyboardInterrupt:
    print("\nTest stopped.")


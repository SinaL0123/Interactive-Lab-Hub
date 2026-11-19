# Escape Together — Final Project

A two-player cooperative puzzle game with a browser-based virtual environment and physical inputs. This folder currently archives the hardware input proof of concept, rather than the finished game.

Course brief: [FinalProject.md](../FinalProject.md)  
Project plan: [Google Doc](https://docs.google.com/document/d/1PFp_F4K3la4clmsv9ACkXorqtDHbX2RVgfYLTaRujgQ/edit)

## Current progress

Sina Liu worked on connecting physical inputs to the Raspberry Pi, verifying readings, and transmitting them to a Mac browser.

The following were reported working during the November 18 hardware session:

- One Qwiic button: press and release.
- One Adafruit rotary encoder: count changes in both directions.
- One Qwiic joystick: horizontal, vertical and push-button readings.
- Combined input readings displayed in a Mac browser over WebSocket.

These are development checks, not formal user playtests. The available quantities describe this test setup, not the final project's total hardware requirements or a change to the overall game plan.

The Python files are archived from the code tested in the accompanying development conversation; they were not downloaded from the Pi. The English HTML page was copied from the local working test page. No new physical hardware test was performed while preparing this archive.

## Hardware and connections

| Component | Quantity in this test | Role / address |
| --- | ---: | --- |
| Raspberry Pi 5 with OS storage and suitable supply | 1 | Reads inputs and runs Python server |
| SparkFun Pi Servo pHAT | 1 | GPIO-mounted expansion board with Qwiic port |
| SparkFun Qwiic Button | 1 | Input at 0x6F |
| Adafruit STEMMA QT / seesaw rotary encoder | 1 | Input at 0x36 |
| SparkFun Qwiic Joystick COM-15168 | 1 | Input at 0x20 |
| Qwiic cables | 3 | Board-to-board connections |
| Mac / display computer | 1 | Browser client on the same local network |

With the Pi shut down and power disconnected, mount the pHAT on the 40-pin GPIO header with correct pin-1 alignment and clearance from metal parts. The small Mini PiTFT was removed for this setup.

Connect the Qwiic ports in this order:

**Pi Servo pHAT → button → encoder → joystick**

The modules share an I²C bus; the order is the physical cable layout, not a software data-processing chain. Power the Pi through its own USB-C power input. This prototype does not use the pHAT's servo outputs or its USB-C connector.

Enable I²C using `sudo raspi-config` → Interface Options → I2C → Yes. Then scan:

```bash
sudo apt install -y i2c-tools
sudo i2cdetect -y 1
```

The combined setup scan showed `20`, `36`, `40`, `6f` and `70`. The `40` and `70` entries are associated with the pHAT PWM controller; the game inputs use `20`, `36` and `6f`. Assign distinct addresses before adding a second same-address module, particularly another Qwiic Button.

## Files

| File | Purpose |
| --- | --- |
| `button_server.py` | Combined hardware reader and WebSocket server; filename retained from first button prototype |
| `button_test.html` | English browser monitor for all three input types |
| `test_button.py` | Standalone button check |
| `test_encoder.py` | Standalone rotary encoder check |
| `test_joystick.py` | Standalone joystick check |
| `requirements.txt` | Dependencies, including the optional proximity sensor driver |
| `docs/progress.md` | Development log, remaining deliverables and planned validation |

## Install on Raspberry Pi

After cloning this repository on the Pi, run these commands from this folder:

```bash
sudo apt update
sudo apt install -y python3-venv i2c-tools
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Python 3.11 was used during development. Observed installed versions included Adafruit-Blinka 10.2.0, adafruit-circuitpython-seesaw 1.18.2 and sparkfun-qwiic-button 2.0.3. Other exact versions were not recorded, so requirements.txt is not a frozen environment.

Run standalone checks one at a time, stopping each with Ctrl+C:

```bash
python test_button.py
python test_encoder.py
python test_joystick.py
```

## Run the combined demo

On the Pi, from this folder with the virtual environment active:

```bash
python button_server.py
```

Leave the program running after `Server ready on port 8765` appears. Find the Pi's local IP with `hostname -I`.

On the Mac, open `button_test.html` in a browser (or run `open button_test.html` from this folder). Enter the Pi IP and click **Connect**. Allow local-network access if prompted. The Mac and Pi must have local network connectivity.

The browser connects to `ws://<PI_IP>:8765`. This is a local development server without authentication or TLS; do not expose its port to the internet. GitHub stores the files; it does not run the hardware server.

## Data format

The server sends a JSON message approximately every 50 ms, with timing also dependent on hardware reads:

```json
{
  "button": false,
  "encoder": -8,
  "joystick": {
    "x": 512,
    "y": 512,
    "pressed": false
  }
}
```

- `button`: true while the separate Qwiic button is pressed.
- `encoder`: relative count, initialized to zero when the server starts; not degrees. Refreshing the webpage does not reset it.
- `joystick.x` / `y`: raw 10-bit readings, nominally 0–1023. Center readings need calibration; small variations are expected.
- `joystick.pressed`: true while the stick is pressed down.

The frontend can map these raw inputs to game state. Calibration, joystick dead zones and game-specific mappings remain future integration work.

## Troubleshooting

- **ModuleNotFoundError:** activate `.venv` and install requirements using that environment's `python -m pip`.
- **Device not detected:** shut down and disconnect power before checking cables and header alignment; confirm addresses with `i2cdetect`.
- **Webpage cannot connect:** confirm the server is running, current Pi IP, local network access and port 8765.
- **Address already in use:** stop the earlier server with Ctrl+C before starting another instance.
- **Readings stop:** check the Pi terminal for an I²C error. This prototype does not yet recover automatically from hardware faults.
- The VCNL4040 Python driver is `adafruit-circuitpython-vcnl4040` (import `adafruit_vcnl4040`), not the unavailable package `sparkfun-qwiic-vcnl4040`.

## Course milestones and remaining documentation

Per [the course brief](../FinalProject.md):

- **Week of December 1:** functional check-off.
- **December 7:** final presentation.
- **December 14:** write-up and documentation due.

Still to add: original concept sketches, design iteration photos, final game code and control mappings, repeatable user-test plan and observations, user-testing video, reflections, complete team contributions and the group work distribution questionnaire. The course specifies no AI assistance for initial conceptual sketches/notes; those original materials must be contributed by the team.

See [progress and planned validation](docs/progress.md). Unfinished deliverables are not claimed as complete.


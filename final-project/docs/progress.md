# Development progress

## November 18 — Hardware input proof of concept

**Contributor:** Sina Liu — hardware setup, input testing and Pi-to-browser integration.

1. Removed the Mini PiTFT to free the GPIO header and mounted the Pi Servo pHAT.
2. Connected one Qwiic Button and confirmed address 0x6F.
3. Verified button press/release in an SSH terminal, then in a Mac webpage.
4. Added the Adafruit seesaw encoder, confirmed 0x36, and verified relative counts locally and in the browser.
5. Added the Qwiic Joystick, confirmed 0x20, and verified X, Y and press readings.
6. Combined button, encoder and joystick data in one WebSocket message; all three input types were reported working in the browser.
7. Changed the browser interface to English.

The first proposed VCNL4040 package name was unavailable. It was replaced by adafruit-circuitpython-vcnl4040. The proximity sensor itself has not yet been validated in this combined prototype.

## Planned validation — not yet recorded as complete

| Check | Procedure | Expected result |
| --- | --- | --- |
| Simultaneous input | Operate button, encoder and joystick together for several minutes | Browser values update; no exceptions or freeze |
| Browser reconnection | Close and reopen the page while leaving server running | Connect restores live readings |
| Restart | Stop server and restart it | Reconnect works; encoder starts at zero |
| Calibration | Record joystick center and extremes | Choose dead zone and axis mapping from measurements |
| Pair playtest | Test an implemented cooperative challenge with two people | Document communication, participation, errors and difficulty |

## Materials still needed

- Original concept sketches/notes and development photos.
- Full team roster and division of work beyond this hardware session.
- Game integration and final control mappings.
- User-test procedure, observations, revisions and demonstration video.
- Final reflections and work distribution questionnaire.

No formal user study, latency measurement or long-duration reliability result is claimed in this archive.


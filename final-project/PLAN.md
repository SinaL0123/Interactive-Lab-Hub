# Escape Together: Project Plan

## 1. Team / Project Name

**Project name:** Escape Together  
**Team members:** Jindi Chai (jc3892), Sina Liu (sl3733)

## 2. Team Responsibilities

Both members will contribute to technical implementation, interaction design, testing, and documentation.

**Sina** will lead hardware setup, input calibration, and data collection on the Raspberry Pi 5. They will also implement part of the shared game logic and document the hardware and communication setup.

**Jindi** will lead the browser-based interface and visual feedback, including the facial animation and navigation display. They will also implement input-to-game mappings, integrate the data received from the Raspberry Pi, and document the software and interaction design.

We will jointly develop the puzzle rules, integrate the hardware and software, conduct playtests, and prepare the final documentation and demonstration. We will review each other’s work so that both members understand the complete system.

## 3. Big Idea

Escape Together is a two-player cooperative puzzle game inspired by escape rooms. The escape setting and puzzles will primarily appear in a virtual interface, while players interact through physical sensors or controllers. We are not planning to construct a full physical room. The final display and controller form will be determined through prototyping.

Our central goal is to make cooperation necessary. Rather than giving each player an independent task, we will design interactions in which one player’s actions affect what the other needs to do.

To keep the project manageable, we will build a shared system for processing two players’ inputs, updating the game state, providing feedback, and checking success conditions. The challenges will reuse this system with different visual representations and interaction rules. Rotary encoders, joysticks, and buttons can provide different physical interactions across challenges while sharing the same input and communication system.

### Challenge 1: Face Calibration

Players work together to match a target facial expression using the eyes and mouth. Both controllers will influence both features in different ways. For example, one input could increase both eye opening and mouth curvature, while the other increases eye opening but decreases mouth curvature.

Because adjusting either controller affects the shared expression, players must coordinate and compensate for each other’s actions. They must maintain the matching expression briefly to complete the challenge. Rotary encoders are the initial input option for this challenge; we will test and refine these mappings to keep them understandable.

### Challenge 2: Coordinate Navigation

One player controls an object’s horizontal velocity, while the other controls its vertical velocity. Together, they must guide it through a path toward an exit. Joysticks are the initial input option: the game will use only each player’s assigned axis. An on-screen indicator will show the current velocity and zero-speed setting. We will calibrate the neutral position and apply a dead zone to reduce drift.

Diagonal sections will require continuous input from both players. Moving along only one axis will take the object outside the path, encouraging players to coordinate their timing and movement speed.

### Challenge 3: Exit Unlock

One player receives unlocking instructions hidden from the other and must maintain a required controller state. The other follows those instructions to adjust their controller and press a physical button to submit an action. Players will exchange roles between stages.

This challenge combines information sharing with simultaneous physical interaction, giving both players an active role. It can reuse the rotary encoders or joysticks alongside the buttons.

## 4. Project Timeline

| Dates | Stage | Planned work |
| --- | --- | --- |
| November 11–17 | Hardware Confirmation & Interaction Prototyping | Identify the available Qwiic cables, adapter, and input modules. Acquire missing components and test readings on the Raspberry Pi 5. Prototype face calibration using simulated inputs while hardware setup is in progress, and test whether the controls encourage cooperation. |
| November 18–24 | Hardware Integration & Core Development | Verify button, rotary encoder, and joystick readings and transmit them to a browser test page. Acquire additional modules needed for the two-player setup. Implement input calibration, visual feedback, success detection, and game reset. Complete face calibration and develop coordinate navigation using the shared game system. |
| November 25–30 | Complete Gameplay & Playtesting | Connect the challenges into a complete game and add the exit challenge if the core experience is stable. Conduct playtests with pairs of players to evaluate cooperation, difficulty, instructions, and sensor responsiveness. |
| December 1–6 | Functional Check-off & Refinement | Demonstrate the core technical loop to the teaching team during the week of December 1. Address playtest issues, secure the controls, verify the complete game, and collect documentation and user-testing video. |
| December 7 | Final Presentation | Present the functioning game in class and prepare it for participants to try. |
| December 8–14 | Final Documentation | Complete the design-process write-up, code archive, user-testing video, reflections, and work distribution questionnaire. Submit the write-up and documentation by December 14. |

## 5. Hardware and Data Collection

We already have a Raspberry Pi 5, Qwiic cables, and a SparkFun Pi Servo pHAT with a Qwiic connection. Our input options include SparkFun Qwiic Buttons, Adafruit STEMMA QT / seesaw rotary encoders, and SparkFun Qwiic Joysticks. A VCNL4040 proximity sensor is also available as an optional input for testing hand proximity.

We will build two player control stations and reuse the modules across challenges. The current hardware kit is an initial test set, not the complete project inventory. We can request additional modules from the TA after confirming the final controller layout; the overall game plan is not limited by the quantities currently in hand.

| Component | Planned quantity / status | Purpose |
| --- | --- | --- |
| Raspberry Pi 5 with compatible power supply and system storage | 1 set; available | Reads physical inputs and runs the game server |
| SparkFun Pi Servo pHAT | 1; available | Provides the Pi-to-Qwiic connection; servo outputs are not required for the current prototype |
| I²C rotary encoder modules | Target: 2, one per player; additional modules can be requested | Continuous adjustments, initially for face calibration |
| SparkFun Qwiic Joysticks | Target: 2, one per player; additional modules can be requested | Horizontal/vertical navigation using one assigned axis per player |
| SparkFun Qwiic Buttons | Target: at least 2, one per player | Confirmation and submission actions, reusable across challenges |
| VCNL4040 proximity sensor | 1 available for optional exploration; more only if selected | Alternative continuous input based on hand proximity |
| Qwiic / compatible STEMMA QT cables | Enough for all selected modules and the two-player layout | Power and I²C connections; the present three-input test uses three cables |
| Controller housings and mounting materials | 2 sets | Secure and separate the two players’ controls |
| Existing computer and display | 1 set | Displays the shared browser-based game |

The Raspberry Pi will read the modules over I²C through the pHAT’s Qwiic port. Modules can be chained with Qwiic cables. We will configure distinct I²C addresses when using multiple modules that share a default address.

A Python program will send button states, encoder counts, and joystick readings to the browser-based game over a local WebSocket connection, with the Raspberry Pi and display computer on the same local network. The browser will map the inputs to the current challenge, allowing the hardware input layer to remain shared across the game.

The initial test uses addresses 0x6F for the button, 0x36 for the encoder, and 0x20 for the joystick. These are the current prototype’s addresses; additional matching devices must be configured separately before being connected together. Encoder readings are relative counts rather than absolute angles, and joystick inputs will be calibrated before mapping to movement.

Cameras and microphones are not required because we will not use facial or speech recognition. These I²C input modules do not require a separate external analog-to-digital converter. The small Mini PiTFT display and speaker are optional future outputs, not dependencies of the current browser-based prototype.

**Hardware progress, November 18:** button, encoder, and joystick readings have been individually tested and displayed together in the computer’s browser through WebSocket. The proximity sensor and additional duplicate modules remain to be tested. See the [hardware setup and code](README.md) and [development log](docs/progress.md).

## 6. Fall-Back Plan

Our minimum complete version will include two polished challenges—face calibration and coordinate navigation—using the same two player control stations. If time is limited, we will simplify or remove the third challenge and use an on-screen escape sequence as the ending.

If a selected module is unavailable or unreliable, we will request a replacement from the TA or substitute another tested input type while preserving the two players’ complementary roles. Rotary encoders and joysticks can be mapped to the same normalized control values. A further backup is to use rotary potentiometers with a compatible analog-to-digital converter; unlike the I²C modules, these require additional analog input hardware.

Keyboard inputs will remain available for software development and troubleshooting while hardware issues are resolved. If network connectivity is unreliable, we will test running the browser interface directly on the Raspberry Pi with a connected display.

Across these adjustments, we will preserve the project’s central feature: two players must coordinate their physical inputs to achieve a shared goal.

---

Updated from the supplied **IDD Final Project Plan**. Changes focus on the confirmed hardware options, current input-testing progress, related controller wording, and the milestones in the [course brief](../FinalProject.md). The three-challenge concept and team responsibilities are retained.

